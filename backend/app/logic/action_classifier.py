from __future__ import annotations

import numpy as np

from .smoothing_rules import remove_action
from .filling_rules import fill_action
from .risk_engine import zone_risk


def classify(zone_id: str, devs: np.ndarray, tolerance: float, material: str, scan_quality: str, recon_confidence: str) -> dict:
    mean = float(np.mean(devs))
    max_d = float(np.max(devs))

    if mean > tolerance:
        action, grit, severity, notes = remove_action(mean, material)
        tool = {
            "wood": "orbital sander / smoothing block",
            "plastic": "fine smoothing block",
            "metal": "file / deburring tool",
            "plaster/drywall": "smoothing sponge",
            "unknown": "smoothing block",
        }.get(material, "smoothing block")
        logical_action = "REMOVE"
    elif mean < -tolerance:
        action, grit, notes = fill_action(material)
        severity = "FILL"
        tool = "filler applicator + smoothing block"
        logical_action = "FILL"
    else:
        logical_action = "KEEP"
        action = "verify"
        severity = "KEEP"
        tool = "inspection"
        grit = [220, 320]
        notes = ["No correction needed.", "Rescan to verify before removing material."]

    risk = zone_risk(mean, scan_quality, recon_confidence)

    return {
        "id": zone_id,
        "label": zone_id.replace("_", " ").title(),
        "mean_deviation_mm": round(mean, 3),
        "max_deviation_mm": round(max_d, 3),
        "action": logical_action,
        "severity": severity,
        "tool": tool,
        "grit": grit,
        "risk": risk["risk_level"],
        "instructions": [f"Primary action: {action}", *notes, *risk["warnings"]],
    }
