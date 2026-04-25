from __future__ import annotations

import uuid
from pathlib import Path
import shutil

from fastapi import UploadFile

from app.models.schemas import JobStatus
from app.services.scan_session_service import SCAN_SESSIONS
from app.services.reconstruction_service import reconstruct
from app.services.comparison_service import compare_scan_to_reference
from app.services.report_service import save_reports
from app.storage.file_store import SCANS, result_dir

JOBS: dict[str, JobStatus] = {}
JOB_CONTEXT: dict[str, dict] = {}
RESULTS: dict[str, dict] = {}


def start_processing(scan_id: str) -> dict:
    if scan_id not in SCAN_SESSIONS:
        raise KeyError("scan not found")
    job_id = str(uuid.uuid4())
    JOBS[job_id] = JobStatus(job_id=job_id, scan_id=scan_id, stage="reconstructing", progress=20, message="Building reconstruction")
    recon = reconstruct(scan_id, str(SCANS / scan_id / "images"))
    JOBS[job_id].stage = "awaiting_reference"
    JOBS[job_id].progress = 55
    JOBS[job_id].message = "Reference input required"
    JOB_CONTEXT[job_id] = {"scan_id": scan_id, "reconstruction": recon}
    return {"job_id": job_id, "status": "processing"}


def set_reference(job_id: str, material: str, reference_mesh: UploadFile | None, reference_json: dict | None, reference_dimensions: dict | None):
    if job_id not in JOB_CONTEXT:
        raise KeyError("job not found")
    ctx = JOB_CONTEXT[job_id]
    out = Path(result_dir(job_id))
    mesh_path = None
    if reference_mesh:
        mesh_path = out / reference_mesh.filename
        with mesh_path.open("wb") as f:
            shutil.copyfileobj(reference_mesh.file, f)
    ctx.update(
        {
            "reference_mesh_path": str(mesh_path) if mesh_path else None,
            "reference_json": reference_json,
            "reference_dimensions": reference_dimensions,
            "material": material,
        }
    )


def run_compare(job_id: str) -> dict:
    if job_id not in JOB_CONTEXT:
        raise KeyError("job not found")
    ctx = JOB_CONTEXT[job_id]
    scan_id = ctx["scan_id"]
    scan_summary = SCAN_SESSIONS[scan_id].capture_summary.model_dump()
    result = compare_scan_to_reference(
        scan_mesh_path=ctx["reconstruction"]["model_path"],
        reference_mesh_path=ctx.get("reference_mesh_path"),
        reference_json=ctx.get("reference_json"),
        reference_dimensions=ctx.get("reference_dimensions"),
        scan_quality=scan_summary,
        reconstruction=ctx["reconstruction"],
        material=ctx.get("material", "unknown"),
    )
    payload = {"scan_id": scan_id, "reconstruction": ctx["reconstruction"], "scan_quality": scan_summary, **result}
    out = result_dir(payload["result_id"])
    json_path, pdf_path = save_reports(out, payload)
    payload.update(
        {
            "report_json_url": f"/api/result/{payload['result_id']}/report.json",
            "report_pdf_url": f"/api/result/{payload['result_id']}/report.pdf",
            "_json_path": str(json_path),
            "_pdf_path": str(pdf_path),
        }
    )
    RESULTS[payload["result_id"]] = payload
    JOBS[job_id].stage = "completed"
    JOBS[job_id].progress = 100
    JOBS[job_id].message = "Comparison complete"
    JOBS[job_id].status = "completed"
    return {"result_id": payload["result_id"]}
