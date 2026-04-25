from __future__ import annotations

import numpy as np


def segment_into_zones(points: np.ndarray, divisions: int = 2) -> list[dict]:
    mins = points.min(axis=0)
    maxs = points.max(axis=0)
    step = (maxs - mins) / divisions

    zones = []
    zone_id = 1
    for ix in range(divisions):
        for iy in range(divisions):
            for iz in range(divisions):
                low = mins + np.array([ix, iy, iz]) * step
                high = low + step
                mask = np.all((points >= low) & (points <= high), axis=1)
                idx = np.where(mask)[0]
                if len(idx) == 0:
                    continue
                zones.append(
                    {
                        "id": f"zone_{zone_id}",
                        "indices": idx,
                        "bbox": [low.tolist(), high.tolist()],
                    }
                )
                zone_id += 1
    return zones
