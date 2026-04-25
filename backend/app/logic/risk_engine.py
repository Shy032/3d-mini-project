from __future__ import annotations


def zone_risk(mean_dev: float, scan_quality: str, confidence: str) -> dict:
    warnings = []
    if mean_dev > 2.0:
        warnings.append("High removal depth >2mm")
    if mean_dev < -1.0:
        warnings.append("Area may already be below target")
    if scan_quality == "LOW":
        warnings.append("Scan quality is low, measurement may be unreliable.")
    if confidence == "LOW":
        warnings.append("Low confidence reconstruction")
    level = "HIGH" if len(warnings) >= 2 else "MEDIUM" if len(warnings) == 1 else "LOW"
    return {"risk_level": level, "warnings": warnings}
