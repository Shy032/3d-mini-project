from __future__ import annotations

from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.scan_session_service import SCAN_SESSIONS, create_scan_session, add_frame, finish_scan
from app.services.job_service import start_processing
from app.storage.file_store import scan_dir

router = APIRouter(prefix="/api/scan", tags=["scan"])


@router.post("/start")
def start_scan():
    session = create_scan_session()
    return {"scan_id": session.scan_id}


@router.post("/{scan_id}/frame")
def upload_frame(scan_id: str, file: UploadFile = File(...)):
    if scan_id not in SCAN_SESSIONS:
        raise HTTPException(status_code=404, detail="scan not found")
    d = scan_dir(scan_id) / "images"
    filename = f"frame_{len(SCAN_SESSIONS[scan_id].frames)+1:03d}.jpg"
    path = d / filename
    with path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    frame, _summary = add_frame(scan_id, path, filename)
    return {
        "frame_id": frame.frame_id,
        "accepted": frame.accepted,
        "quality": {
            "blur_score": frame.quality.blur_score,
            "brightness": frame.quality.brightness,
            "warnings": frame.quality.warnings,
        },
    }


@router.post("/{scan_id}/finish")
def finish(scan_id: str):
    if scan_id not in SCAN_SESSIONS:
        raise HTTPException(status_code=404, detail="scan not found")
    session = finish_scan(scan_id)
    return {
        "scan_id": scan_id,
        "frame_count": session.capture_summary.frame_count,
        "accepted_frame_count": session.capture_summary.accepted_frame_count,
        "scan_quality": session.capture_summary.quality,
        "next_step": "process",
    }


@router.post("/{scan_id}/process")
def process_scan(scan_id: str):
    try:
        return start_processing(scan_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="scan not found")
