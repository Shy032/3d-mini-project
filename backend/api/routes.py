from __future__ import annotations

from pathlib import Path
import shutil
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from .models import CompareRequest, CompareResult, DimensionReference, ReferenceSpec
from core.file_loader import load_mesh
from core.converter import mesh_to_point_cloud
from core.scaler import normalize_mesh_scale
from geometry.align import align_icp
from geometry.deviation import compute_signed_deviation
from geometry.segmentation import segment_into_zones
from logic.action_classifier import classify_zone, build_steps
from logic.scan_quality import evaluate_scan_quality
from output.report_generator import save_json_report, save_pdf_report

router = APIRouter(prefix="/api")

BASE_DIR = Path(__file__).resolve().parents[1]
UPLOADS_DIR = BASE_DIR / "data" / "uploads"
JOBS_DIR = BASE_DIR / "jobs"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
JOBS_DIR.mkdir(parents=True, exist_ok=True)

IN_MEMORY_RESULTS: dict[str, dict] = {}


def _build_dimension_box_mesh(dim: DimensionReference):
    import trimesh

    box = trimesh.creation.box(extents=(dim.width, dim.height, dim.depth))
    return box


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "SandingGuide AI backend"}


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    destination = UPLOADS_DIR / f"{uuid.uuid4()}_{file.filename}"
    with destination.open("wb") as out:
        shutil.copyfileobj(file.file, out)
    return {"file": str(destination)}


@router.post("/compare", response_model=CompareResult)
async def compare(
    scan_file: str = Form(...),
    reference_file: str | None = Form(None),
    reference_spec_json: str | None = Form(None),
    dimension_reference_json: str | None = Form(None),
):
    import json

    try:
        spec = ReferenceSpec.model_validate_json(reference_spec_json) if reference_spec_json else None
        dims = DimensionReference.model_validate_json(dimension_reference_json) if dimension_reference_json else None
        req = CompareRequest(
            scan_file=scan_file,
            reference_file=reference_file,
            reference_spec=spec,
            dimension_reference=dims,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {e}")

    scan_mesh = load_mesh(req.scan_file)

    if req.reference_file:
        reference_mesh = load_mesh(req.reference_file)
    elif req.dimension_reference:
        reference_mesh = _build_dimension_box_mesh(req.dimension_reference)
    else:
        raise HTTPException(status_code=400, detail="Provide reference_file or dimension_reference_json")

    if req.reference_spec and req.reference_spec.known_scale:
        ks = req.reference_spec.known_scale
        scan_mesh = normalize_mesh_scale(scan_mesh, ks.dimension, ks.value)

    scan_points = mesh_to_point_cloud(scan_mesh)
    reference_points = mesh_to_point_cloud(reference_mesh)

    aligned, icp_metrics = align_icp(scan_points, reference_points)
    signed_deviation, stats = compute_signed_deviation(aligned, reference_points)
    zones = segment_into_zones(aligned, divisions=2)

    tolerance = req.reference_spec.tolerance_mm if req.reference_spec else 0.2
    zone_results = [classify_zone(z["id"], signed_deviation[z["indices"]], tolerance=tolerance) for z in zones]
    steps = build_steps(zone_results)
    scan_quality = evaluate_scan_quality(scan_points, known_scale_present=bool(req.reference_spec and req.reference_spec.known_scale))

    heatmap = []
    for z in zones:
        matched = next(x for x in zone_results if x["id"] == z["id"])
        heatmap.append({"zone": z["id"], "bbox": z["bbox"], "deviation": matched["deviation"], "action": matched["action"]})

    summary = {
        **stats,
        "icp": icp_metrics,
        "zone_count": len(zone_results),
        "remove_zones": sum(1 for z in zone_results if z["action"] == "REMOVE"),
        "fill_zones": sum(1 for z in zone_results if z["action"] == "FILL"),
    }

    result_payload = {
        "zones": zone_results,
        "steps": steps,
        "scan_quality": scan_quality,
        "summary": summary,
        "heatmap": heatmap,
    }

    job_id = str(uuid.uuid4())
    job_dir = JOBS_DIR / job_id
    json_path = save_json_report(job_dir / "result.json", result_payload)
    pdf_path = save_pdf_report(job_dir / "report.pdf", result_payload)

    result_payload["report_json_path"] = str(json_path)
    result_payload["report_pdf_path"] = str(pdf_path)
    IN_MEMORY_RESULTS[job_id] = result_payload
    return result_payload


@router.get("/result/{job_id}")
def get_job_result(job_id: str) -> dict:
    result = IN_MEMORY_RESULTS.get(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return result
