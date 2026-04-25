from __future__ import annotations

import numpy as np


def _align_centroids(src: np.ndarray, tgt: np.ndarray) -> np.ndarray:
    src_center = src.mean(axis=0)
    tgt_center = tgt.mean(axis=0)
    return src + (tgt_center - src_center)


def align_icp(scan_points: np.ndarray, reference_points: np.ndarray) -> tuple[np.ndarray, dict]:
    try:
        import open3d as o3d  # type: ignore

        src = o3d.geometry.PointCloud()
        src.points = o3d.utility.Vector3dVector(scan_points)
        tgt = o3d.geometry.PointCloud()
        tgt.points = o3d.utility.Vector3dVector(reference_points)

        threshold = max(np.linalg.norm(reference_points.std(axis=0)) * 0.15, 1.0)
        reg = o3d.pipelines.registration.registration_icp(
            src,
            tgt,
            threshold,
            np.eye(4),
            o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        )

        transform = reg.transformation
        homog = np.c_[scan_points, np.ones(len(scan_points))]
        aligned = (transform @ homog.T).T[:, :3]
        return aligned, {"fitness": float(reg.fitness), "rmse": float(reg.inlier_rmse)}
    except Exception:
        aligned = _align_centroids(scan_points, reference_points)
        return aligned, {"fitness": 0.0, "rmse": float(np.mean(np.linalg.norm(aligned - reference_points.mean(axis=0), axis=1)))}
