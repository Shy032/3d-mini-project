from __future__ import annotations


def build_repair_plan(zones: list[dict]) -> list[dict]:
    order = {"REMOVE": 0, "FILL": 1, "KEEP": 2}
    zones = sorted(zones, key=lambda z: order[z["action"]])
    steps = []
    i = 1
    for z in zones:
        title = {
            "REMOVE": "Remove / reshape high spots",
            "FILL": "Fill missing regions",
            "KEEP": "Verify stable zones",
        }[z["action"]]
        steps.append(
            {
                "step": i,
                "title": title,
                "zones": [z["id"]],
                "tool": z["tool"],
                "grit": z["grit"][0],
                "instruction": z["instructions"][0],
            }
        )
        i += 1
    return steps
