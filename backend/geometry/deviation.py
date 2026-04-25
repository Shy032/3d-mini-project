from __future__ import annotations

import numpy as np


def compute_signed_deviation(scan_points: np.ndarray, reference_points: np.ndarray) -> tuple[np.ndarray, dict]:
    # nearest-neighbor via brute force (MVP scale, sample-sized)
    diff = scan_points[:, None, :] - reference_points[None, :, :]
    dist = np.linalg.norm(diff, axis=2)
    nearest_idx = np.argmin(dist, axis=1)
    nearest = reference_points[nearest_idx]

    nearest_dist = np.linalg.norm(scan_points - nearest, axis=1)
    ref_centered = nearest - reference_points.mean(axis=0)
    scan_centered = scan_points - reference_points.mean(axis=0)
    sign = np.sign(np.sum(scan_centered * ref_centered, axis=1))
    sign[sign == 0] = 1

    signed = nearest_dist * sign
    metrics = {
        "mean_deviation": float(np.mean(signed)),
        "max_deviation": float(np.max(signed)),
        "min_deviation": float(np.min(signed)),
    }
    return signed, metrics
