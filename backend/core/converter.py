from __future__ import annotations

import numpy as np
import trimesh


def mesh_to_point_cloud(mesh: trimesh.Trimesh, sample_points: int = 8000) -> np.ndarray:
    points, _ = trimesh.sample.sample_surface_even(mesh, sample_points)
    return points
