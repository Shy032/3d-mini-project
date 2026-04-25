from __future__ import annotations

import os

from app.providers.mock_reconstruction_provider import MockReconstructionProvider
from app.providers.colmap_reconstruction_provider import ColmapReconstructionProvider


def reconstruct(scan_id: str, image_dir: str) -> dict:
    use_colmap = os.getenv("TRUEFORM_RECON_PROVIDER", "mock") == "colmap"
    if use_colmap:
        try:
            res = ColmapReconstructionProvider().reconstruct(scan_id, image_dir)
            return res.__dict__
        except Exception as e:
            if os.getenv("TRUEFORM_DEV_FALLBACK", "1") == "1":
                mock = MockReconstructionProvider().reconstruct(scan_id, image_dir)
                d = mock.__dict__
                d["warning"] = f"COLMAP unavailable/failing ({e}). Used mock reconstruction."
                return d
            raise
    return MockReconstructionProvider().reconstruct(scan_id, image_dir).__dict__
