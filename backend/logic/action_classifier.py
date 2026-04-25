from __future__ import annotations

import numpy as np

from .smoothing_rules import smoothing_recommendation
from .filling_rules import filling_recommendation
from .risk_engine import evaluate_risk


def classify_zone(zone_id: str, zone_deviation: np.ndarray, tolerance: float = 0.2) -> dict:
    mean_dev = float(np.mean(zone_deviation))

    if mean_dev > tolerance:
        action = "REMOVE"
        tool, grit, level = smoothing_recommendation(mean_dev)
    elif mean_dev < -tolerance:
        action = "FILL"
        fill = filling_recommendation()
        tool = fill["tool"]
        grit = fill["grit"]
        level = fill["level"]
    else:
        action = "KEEP"
        tool, grit, level = smoothing_recommendation(mean_dev)

    risk, warning = evaluate_risk(mean_dev, level)

    return {
        "id": zone_id,
        "deviation": round(mean_dev, 4),
        "action": action,
        "level": level,
        "tool": tool,
        "grit": grit,
        "risk": risk,
        "warning": warning,
    }


def build_steps(zones: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, int], list[str]] = {}
    for zone in zones:
        key = (zone["action"], zone["tool"], zone["grit"][0])
        grouped.setdefault(key, []).append(zone["id"])

    priority = {"REMOVE": 0, "FILL": 1, "KEEP": 2}
    ordered = sorted(grouped.items(), key=lambda item: (priority[item[0][0]], item[0][2]))

    steps: list[dict] = []
    for i, ((action, tool, grit), zone_ids) in enumerate(ordered, start=1):
        action_name = {
            "REMOVE": "material removal",
            "FILL": "filling",
            "KEEP": "finish pass",
        }[action]
        steps.append({"step": i, "action": action_name, "tool": tool, "grit": grit, "zones": zone_ids})
    return steps
