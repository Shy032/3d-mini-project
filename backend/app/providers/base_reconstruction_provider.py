from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ReconstructionResult:
    provider: str
    model_path: str
    confidence: str
    warning: str | None = None


class ReconstructionProvider:
    def reconstruct(self, scan_id: str, image_dir: str) -> ReconstructionResult:
        raise NotImplementedError
