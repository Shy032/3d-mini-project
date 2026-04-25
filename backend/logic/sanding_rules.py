from __future__ import annotations


def smoothing_recommendation(deviation: float) -> tuple[str, list[int], str]:
    if deviation > 2.0:
        return "rasp / rotary tool", [60, 80], "HEAVY REMOVE"
    if deviation > 1.0:
        return "orbital sander", [80, 120], "MEDIUM REMOVE"
    if deviation > 0.5:
        return "orbital sander", [120, 180], "LIGHT REMOVE"
    if deviation > 0.2:
        return "hand smoothing block", [180, 220], "FINE REMOVE"
    return "finish smoothing", [220, 320], "ACCEPTABLE"
