from __future__ import annotations

import numpy as np


def evaluate_scan_quality(points: np.ndarray, known_scale_present: bool) -> dict:
    issues: list[str] = []
    suggestions: list[str] = []

    if len(points) < 1500:
        issues.append("low point density")
        suggestions.append("capture from more angles or increase scan resolution")

    spread = points.max(axis=0) - points.min(axis=0)
    if np.any(spread < 1e-2):
        issues.append("possible missing regions")
        suggestions.append("ensure full coverage around object")

    if not known_scale_present:
        issues.append("scale ambiguity")
        suggestions.append("provide known scale dimension in reference")

    if len(issues) >= 2:
        quality = "LOW"
    elif len(issues) == 1:
        quality = "MEDIUM"
    else:
        quality = "HIGH"

    return {"quality": quality, "issues": issues, "suggestions": suggestions}
