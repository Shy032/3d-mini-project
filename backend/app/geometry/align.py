from __future__ import annotations

import numpy as np


def align_icp(scan_points: np.ndarray, reference_points: np.ndarray) -> tuple[np.ndarray, dict]:
    try:
        import open3d as o3d  # type: ignore

        src = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(scan_points))
        tgt = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(reference_points))
        reg = o3d.pipelines.registration.registration_icp(
            src, tgt, 5.0, np.eye(4), o3d.pipelines.registration.TransformationEstimationPointToPoint()
        )
        t = reg.transformation
        aligned = (t @ np.c_[scan_points, np.ones(len(scan_points))].T).T[:, :3]
        return aligned, {"fitness": float(reg.fitness), "rmse": float(reg.inlier_rmse)}
    except Exception:
        delta = reference_points.mean(axis=0) - scan_points.mean(axis=0)
        aligned = scan_points + delta
        return aligned, {"fitness": 0.0, "rmse": float(np.mean(np.linalg.norm(aligned - reference_points.mean(axis=0), axis=1)))}
