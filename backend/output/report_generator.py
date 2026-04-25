from __future__ import annotations

from pathlib import Path
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def save_json_report(output_path: Path, payload: dict) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    return output_path


def save_pdf_report(output_path: Path, payload: dict) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output_path), pagesize=letter)
    width, height = letter

    y = height - 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "SandingGuide AI Report")
    y -= 24

    c.setFont("Helvetica", 10)
    summary = payload.get("summary", {})
    c.drawString(40, y, f"Mean deviation: {summary.get('mean_deviation', 'n/a')} mm")
    y -= 14
    c.drawString(40, y, f"Max deviation: {summary.get('max_deviation', 'n/a')} mm")
    y -= 14
    c.drawString(40, y, f"Min deviation: {summary.get('min_deviation', 'n/a')} mm")
    y -= 24

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Zone actions")
    y -= 16
    c.setFont("Helvetica", 9)

    for zone in payload.get("zones", []):
        line = f"{zone['id']}: {zone['action']} ({zone['deviation']} mm), {zone['tool']}, grit {zone['grit']}"
        c.drawString(40, y, line[:120])
        y -= 12
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()
    return output_path
