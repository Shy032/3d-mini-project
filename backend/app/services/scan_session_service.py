from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import uuid

from app.models.schemas import ScanSession, FrameRecord, FrameQuality, CaptureSummary
from app.storage.file_store import scan_dir
from .frame_quality_service import evaluate_frame

SCAN_SESSIONS: dict[str, ScanSession] = {}


def create_scan_session() -> ScanSession:
    scan_id = str(uuid.uuid4())
    scan_dir(scan_id)
    session = ScanSession(scan_id=scan_id)
    SCAN_SESSIONS[scan_id] = session
    return session


def add_frame(scan_id: str, image_path: Path, filename: str) -> tuple[FrameRecord, CaptureSummary]:
    session = SCAN_SESSIONS[scan_id]
    q = evaluate_frame(image_path)

    frame = FrameRecord(
        frame_id=str(uuid.uuid4()),
        filename=filename,
        timestamp=datetime.now(timezone.utc).isoformat(),
        quality=FrameQuality(blur_score=q["blur_score"], brightness=q["brightness"], warnings=q["warnings"]),
        accepted=q["accepted"],
    )
    session.frames.append(frame)
    session.capture_summary = _compute_summary(session)
    return frame, session.capture_summary


def finish_scan(scan_id: str) -> ScanSession:
    session = SCAN_SESSIONS[scan_id]
    session.status = "uploaded"
    session.capture_summary = _compute_summary(session)
    return session


def _compute_summary(session: ScanSession) -> CaptureSummary:
    frame_count = len(session.frames)
    accepted = sum(1 for f in session.frames if f.accepted)
    issues = []
    if accepted < 20:
        quality = "LOW"
        issues.append("too few images")
    elif accepted < 40:
        quality = "MEDIUM"
        issues.append("capture more angles")
    else:
        quality = "GOOD"

    blurry = sum(1 for f in session.frames if "Image too blurry" in f.quality.warnings)
    dark = sum(1 for f in session.frames if "Too dark" in f.quality.warnings)
    if blurry > max(frame_count * 0.3, 5):
        issues.append("many blurry images")
    if dark > max(frame_count * 0.3, 5):
        issues.append("low light")

    return CaptureSummary(frame_count=frame_count, accepted_frame_count=accepted, quality=quality, issues=issues)
