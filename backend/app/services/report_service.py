from __future__ import annotations

from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def save_reports(result_dir: Path, payload: dict) -> tuple[Path, Path]:
    result_dir.mkdir(parents=True, exist_ok=True)
    json_path = result_dir / "report.json"
    pdf_path = result_dir / "report.pdf"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, 760, "TrueForm AI - Flaw Correction Report")
    c.setFont("Helvetica", 10)
    c.drawString(40, 736, f"Result ID: {payload['result_id']}")
    c.drawString(40, 722, f"Overall status: {payload['summary']['overall_status']}")
    y = 700
    for z in payload["zones"][:20]:
        c.drawString(40, y, f"{z['id']}: {z['action']} ({z['mean_deviation_mm']} mm) {z['tool']}")
        y -= 12
    c.save()

    return json_path, pdf_path
