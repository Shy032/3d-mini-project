from __future__ import annotations

from pathlib import Path
import trimesh

SUPPORTED_MESH = {".obj", ".ply", ".stl", ".glb", ".gltf"}


def load_mesh(path: str | Path) -> trimesh.Trimesh:
    p = Path(path)
    if p.suffix.lower() not in SUPPORTED_MESH:
        raise ValueError(f"Unsupported mesh extension: {p.suffix}")
    mesh = trimesh.load(p, force="mesh")
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(mesh.geometry.values()))
    if not isinstance(mesh, trimesh.Trimesh) or mesh.is_empty:
        raise ValueError("Invalid mesh")
    return mesh


def to_points(mesh: trimesh.Trimesh, n: int = 7000):
    pts, _ = trimesh.sample.sample_surface_even(mesh, n)
    return pts


def mesh_from_dimensions(width: float, height: float, depth: float) -> trimesh.Trimesh:
    return trimesh.creation.box(extents=[width, height, depth])
