from __future__ import annotations

from pathlib import Path
import numpy as np
import trimesh


OUT = Path(__file__).resolve().parent


def main() -> None:
    cube = trimesh.creation.box(extents=(100, 100, 100))
    cube.export(OUT / "cube_reference.stl")

    deformed = cube.copy()
    vertices = deformed.vertices.copy()
    top_mask = vertices[:, 2] > 40
    vertices[top_mask, 2] += 2.5
    side_mask = vertices[:, 0] < -40
    vertices[side_mask, 0] -= 1.2
    noise = np.random.normal(scale=0.2, size=vertices.shape)
    vertices += noise
    deformed.vertices = vertices
    deformed.export(OUT / "cube_scan_deformed.stl")

    print("Generated sample files:")
    print(OUT / "cube_reference.stl")
    print(OUT / "cube_scan_deformed.stl")


if __name__ == "__main__":
    main()
