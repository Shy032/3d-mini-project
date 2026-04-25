from __future__ import annotations

import numpy as np
import trimesh


DIMENSION_AXIS = {"width": 0, "height": 1, "depth": 2}


def normalize_mesh_scale(mesh: trimesh.Trimesh, dimension: str, target_value: float) -> trimesh.Trimesh:
    bounds = mesh.bounds
    current = bounds[1] - bounds[0]
    axis = DIMENSION_AXIS[dimension]
    current_value = float(current[axis])
    if current_value <= 1e-9:
        return mesh

    factor = target_value / current_value
    scaled = mesh.copy()
    scaled.vertices = scaled.vertices * factor
    return scaled


def mesh_extent(mesh: trimesh.Trimesh) -> np.ndarray:
    return mesh.bounds[1] - mesh.bounds[0]
