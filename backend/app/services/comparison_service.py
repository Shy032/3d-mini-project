from __future__ import annotations

import uuid
from pathlib import Path
import numpy as np

from app.geometry.mesh_utils import load_mesh, to_points, mesh_from_dimensions
from app.geometry.align import align_icp
from app.geometry.deviation import compute_deviation
from app.geometry.segmentation import segment
from app.logic.action_classifier import classify
from app.logic.repair_plan import build_repair_plan


def compare_scan_to_reference(
    scan_mesh_path: str,
    reference_mesh_path: str | None,
    reference_json: dict | None,
    reference_dimensions: dict | None,
    scan_quality: dict,
    reconstruction: dict,
    material: str,
) -> dict:
    scan_mesh = load_mesh(scan_mesh_path)
    if reference_mesh_path:
        ref_mesh = load_mesh(reference_mesh_path)
        tolerance = 0.2
    elif reference_dimensions:
        ref_mesh = mesh_from_dimensions(reference_dimensions["width"], reference_dimensions["height"], reference_dimensions["depth"])
        tolerance = float(reference_dimensions.get("tolerance_mm", 0.2))
    elif reference_json:
        if "known_scale" in reference_json and reference_json["known_scale"]:
            # keep placeholder support
            pass
        ref_mesh = mesh_from_dimensions(120, 80, 30)
        tolerance = float(reference_json.get("tolerance_mm", 0.2))
    else:
        raise ValueError("Reference input is required")

    scan_pts = to_points(scan_mesh)
    ref_pts = to_points(ref_mesh)
    aligned, icp = align_icp(scan_pts, ref_pts)
    dev, stats = compute_deviation(aligned, ref_pts)

    zones_meta = segment(aligned, div=2)
    zones = [
        classify(z["id"], dev[z["indices"]], tolerance, material, scan_quality["quality"], reconstruction.get("confidence", "LOW"))
        for z in zones_meta
    ]
    repair_plan = build_repair_plan(zones)

    result_id = str(uuid.uuid4())
    summary = {
        "overall_status": "NEEDS_WORK" if any(z["action"] != "KEEP" for z in zones) else "GOOD",
        "max_excess_mm": round(max(z["max_deviation_mm"] for z in zones), 3),
        "max_missing_mm": round(min(z["mean_deviation_mm"] for z in zones), 3),
        "recommended_first_action": repair_plan[0]["title"] if repair_plan else "verify",
        "icp": icp,
        "deviation_stats": stats,
    }

    heatmap = [{"zone": z["id"], "action": z["action"], "bbox": meta["bbox"]} for z, meta in zip(zones, zones_meta)]

    return {
        "result_id": result_id,
        "reference_id": str(uuid.uuid4()),
        "summary": summary,
        "zones": zones,
        "repair_plan": repair_plan,
        "heatmap": heatmap,
    }
