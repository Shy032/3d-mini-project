from __future__ import annotations

from pathlib import Path
import numpy as np
import trimesh

from .base_reconstruction_provider import ReconstructionProvider, ReconstructionResult


class MockReconstructionProvider(ReconstructionProvider):
    def reconstruct(self, scan_id: str, image_dir: str) -> ReconstructionResult:
        out = Path(image_dir).parent / "reconstruction" / "scan_mock.ply"
        sphere = trimesh.creation.icosphere(subdivisions=3, radius=50)
        v = sphere.vertices.copy()
        v[:, 2] += np.sin(v[:, 0] / 12) * 1.4
        v[:, 0] -= np.cos(v[:, 1] / 15) * 0.8
        sphere.vertices = v
        sphere.export(out)
        return ReconstructionResult(provider="mock", model_path=str(out), confidence="MEDIUM", warning="Demo reconstruction used because real reconstruction provider is not installed.")
