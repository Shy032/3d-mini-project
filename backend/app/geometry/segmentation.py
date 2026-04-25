from __future__ import annotations

import numpy as np


def segment(points: np.ndarray, div: int = 2) -> list[dict]:
    mins, maxs = points.min(axis=0), points.max(axis=0)
    step = (maxs - mins) / div
    out = []
    z = 1
    for ix in range(div):
        for iy in range(div):
            for iz in range(div):
                lo = mins + np.array([ix, iy, iz]) * step
                hi = lo + step
                mask = np.all((points >= lo) & (points <= hi), axis=1)
                ids = np.where(mask)[0]
                if len(ids) == 0:
                    continue
                out.append({"id": f"zone_{z}", "indices": ids, "bbox": [lo.tolist(), hi.tolist()]})
                z += 1
    return out
