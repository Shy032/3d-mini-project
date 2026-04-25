from __future__ import annotations


def evaluate_risk(mean_deviation: float, level: str) -> tuple[str, str | None]:
    if mean_deviation > 2.0 or level == "HEAVY REMOVE":
        return "HIGH", "over-correction risk on high-removal area"
    if mean_deviation > 1.0:
        return "MEDIUM", "monitor thickness while smoothing"
    if mean_deviation < -0.8:
        return "MEDIUM", "deep fill zone may shrink after cure"
    return "LOW", None
