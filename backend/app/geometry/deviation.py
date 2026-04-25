from __future__ import annotations

import numpy as np


def compute_deviation(scan_points: np.ndarray, ref_points: np.ndarray) -> tuple[np.ndarray, dict]:
    d = np.linalg.norm(scan_points[:, None, :] - ref_points[None, :, :], axis=2)
    idx = np.argmin(d, axis=1)
    nearest = ref_points[idx]
    nearest_dist = np.linalg.norm(scan_points - nearest, axis=1)
    center = ref_points.mean(axis=0)
    sign = np.sign(np.sum((scan_points - center) * (nearest - center), axis=1))
    sign[sign == 0] = 1
    signed = nearest_dist * sign
    return signed, {
        "mean": float(np.mean(signed)),
        "max": float(np.max(signed)),
        "min": float(np.min(signed)),
    }
