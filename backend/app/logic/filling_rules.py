from __future__ import annotations


def fill_action(material: str) -> tuple[str, list[int], list[str]]:
    filler = {
        "wood": "wood filler",
        "plastic": "epoxy/plastic repair filler",
        "metal": "metal epoxy",
        "plaster/drywall": "joint compound",
        "unknown": "generic filler",
    }.get(material, "generic filler")
    return (
        f"fill missing material ({filler})",
        [180, 220],
        ["Clean area", "Apply filler", "Let cure", "Sand 180→220", "Rescan"],
    )
