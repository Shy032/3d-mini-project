from __future__ import annotations

from pathlib import Path
import trimesh

SUPPORTED_MESH_EXT = {".ply", ".obj", ".stl", ".glb", ".gltf", ".usdz"}


def load_mesh(file_path: str | Path) -> trimesh.Trimesh:
    path = Path(file_path)
    if path.suffix.lower() not in SUPPORTED_MESH_EXT:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    mesh_or_scene = trimesh.load(path, force="mesh")
    if isinstance(mesh_or_scene, trimesh.Scene):
        mesh = trimesh.util.concatenate(tuple(g for g in mesh_or_scene.geometry.values()))
    else:
        mesh = mesh_or_scene

    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("Could not load mesh")

    if mesh.is_empty:
        raise ValueError("Mesh has no geometry")

    return mesh
