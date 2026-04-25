from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal


class KnownScale(BaseModel):
    dimension: Literal["width", "height", "depth"]
    value: float


class ZoneSpec(BaseModel):
    id: str
    type: str = "generic"
    target: str = "match_reference"
    max_allowed_excess_mm: float = 0.2


class ReferenceSpec(BaseModel):
    object_name: str = "example"
    units: str = "mm"
    tolerance_mm: float = 0.2
    known_scale: KnownScale | None = None
    zones: list[ZoneSpec] = Field(default_factory=list)


class DimensionReference(BaseModel):
    object_name: str = "dimension_reference"
    units: str = "mm"
    tolerance_mm: float = 0.2
    width: float
    height: float
    depth: float


class CompareRequest(BaseModel):
    scan_file: str
    reference_file: str | None = None
    reference_spec: ReferenceSpec | None = None
    dimension_reference: DimensionReference | None = None


class ScanQuality(BaseModel):
    quality: Literal["LOW", "MEDIUM", "HIGH"]
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)


class ZoneDecision(BaseModel):
    id: str
    deviation: float
    action: Literal["REMOVE", "FILL", "KEEP"]
    level: str
    tool: str
    grit: list[int]
    risk: Literal["LOW", "MEDIUM", "HIGH"]
    warning: str | None = None


class ProcessingStep(BaseModel):
    step: int
    action: str
    tool: str
    grit: int
    zones: list[str]


class CompareResult(BaseModel):
    zones: list[ZoneDecision]
    steps: list[ProcessingStep]
    scan_quality: ScanQuality
    summary: dict
    heatmap: list[dict]
    report_json_path: str
    report_pdf_path: str
