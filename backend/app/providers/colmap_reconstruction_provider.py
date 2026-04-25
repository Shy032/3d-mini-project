from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from .base_reconstruction_provider import ReconstructionProvider, ReconstructionResult


class ColmapReconstructionProvider(ReconstructionProvider):
    def reconstruct(self, scan_id: str, image_dir: str) -> ReconstructionResult:
        if shutil.which("colmap") is None:
            raise RuntimeError("COLMAP not installed")

        image_path = Path(image_dir)
        out_dir = image_path.parent / "reconstruction" / "colmap"
        out_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "colmap",
            "automatic_reconstructor",
            "--image_path",
            str(image_path),
            "--workspace_path",
            str(out_dir),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"COLMAP failed: {proc.stderr[:300]}")

        # MVP placeholder output path
        return ReconstructionResult(provider="colmap", model_path=str(out_dir), confidence="HIGH")
