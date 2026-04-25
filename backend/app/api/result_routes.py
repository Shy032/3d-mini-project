from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.job_service import RESULTS

router = APIRouter(prefix="/api/result", tags=["result"])


@router.get("/{result_id}")
def get_result(result_id: str):
    if result_id not in RESULTS:
        raise HTTPException(status_code=404, detail="result not found")
    data = RESULTS[result_id].copy()
    data.pop("_json_path", None)
    data.pop("_pdf_path", None)
    return data


@router.get("/{result_id}/report.json")
def report_json(result_id: str):
    if result_id not in RESULTS:
        raise HTTPException(status_code=404, detail="result not found")
    return FileResponse(RESULTS[result_id]["_json_path"], media_type="application/json")


@router.get("/{result_id}/report.pdf")
def report_pdf(result_id: str):
    if result_id not in RESULTS:
        raise HTTPException(status_code=404, detail="result not found")
    return FileResponse(RESULTS[result_id]["_pdf_path"], media_type="application/pdf")
