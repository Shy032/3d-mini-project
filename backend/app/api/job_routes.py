from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.services.job_service import JOBS, set_reference, run_compare

router = APIRouter(prefix="/api/job", tags=["job"])


@router.get("/{job_id}/status")
def job_status(job_id: str):
    if job_id not in JOBS:
        raise HTTPException(status_code=404, detail="job not found")
    s = JOBS[job_id]
    return {"job_id": s.job_id, "stage": s.stage, "progress": s.progress, "message": s.message}


@router.post("/{job_id}/reference")
def attach_reference(
    job_id: str,
    material: str = Form("unknown"),
    reference_mesh: UploadFile | None = File(None),
    reference_json: str | None = Form(None),
    reference_dimensions: str | None = Form(None),
):
    import json

    try:
        set_reference(
            job_id,
            material,
            reference_mesh,
            json.loads(reference_json) if reference_json else None,
            json.loads(reference_dimensions) if reference_dimensions else None,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="job not found")
    return {"reference_id": job_id, "accepted": True}


@router.post("/{job_id}/compare")
def compare(job_id: str):
    try:
        return run_compare(job_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="job not found")
