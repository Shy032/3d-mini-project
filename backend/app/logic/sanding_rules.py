from __future__ import annotations


def remove_action(dev: float, material: str) -> tuple[str, list[int], str, list[str]]:
    if dev > 2.0:
        return "remove material", [60, 80], "HEAVY_REMOVE", ["High removal depth. Check often.", "Rescan after short passes."]
    if dev > 1.0:
        return "remove material", [80, 120], "MEDIUM_REMOVE", ["Use controlled passes."]
    if dev > 0.5:
        return "smooth surface", [120, 180], "LIGHT_REMOVE", ["Feather the transition edges."]
    return "smooth surface", [180, 220], "FINE_REMOVE", ["Finish and verify."]
