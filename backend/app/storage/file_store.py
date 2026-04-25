from __future__ import annotations

from pathlib import Path
import json

BASE = Path(__file__).resolve().parents[2] / "storage"
SCANS = BASE / "scans"
JOBS = BASE / "jobs"
RESULTS = BASE / "results"

for d in [SCANS, JOBS, RESULTS]:
    d.mkdir(parents=True, exist_ok=True)


def scan_dir(scan_id: str) -> Path:
    p = SCANS / scan_id
    (p / "images").mkdir(parents=True, exist_ok=True)
    (p / "reconstruction").mkdir(parents=True, exist_ok=True)
    return p


def job_dir(job_id: str) -> Path:
    p = JOBS / job_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def result_dir(result_id: str) -> Path:
    p = RESULTS / result_id
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
