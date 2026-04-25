from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal


class FrameQuality(BaseModel):
    blur_score: float
    brightness: float
    warnings: list[str] = Field(default_factory=list)


class FrameRecord(BaseModel):
    frame_id: str
    filename: str
    timestamp: str
    quality: FrameQuality
    accepted: bool


class CaptureSummary(BaseModel):
    frame_count: int
    accepted_frame_count: int
    quality: Literal["LOW", "MEDIUM", "GOOD"]
    issues: list[str] = Field(default_factory=list)


class ScanSession(BaseModel):
    scan_id: str
    status: Literal["capturing", "uploaded", "processing", "completed", "failed"] = "capturing"
    frames: list[FrameRecord] = Field(default_factory=list)
    capture_summary: CaptureSummary = Field(default_factory=lambda: CaptureSummary(frame_count=0, accepted_frame_count=0, quality="LOW", issues=[]))


class KnownScale(BaseModel):
    dimension: Literal["width", "height", "depth"]
    value: float


class ZoneSpec(BaseModel):
    id: str
    type: str = "flat"
    target: str = "match_reference"
    max_allowed_excess_mm: float = 0.2


class JsonReference(BaseModel):
    object_name: str = "sample"
    units: str = "mm"
    tolerance_mm: float = 0.2
    known_scale: KnownScale | None = None
    zones: list[ZoneSpec] = Field(default_factory=list)


class DimensionReference(BaseModel):
    object_type: Literal["flat_board", "block", "curved", "custom"] = "block"
    units: str = "mm"
    width: float
    height: float
    depth: float
    tolerance_mm: float = 0.2


class JobStatus(BaseModel):
    job_id: str
    scan_id: str
    stage: str = "queued"
    progress: int = 0
    message: str = "waiting"
    status: Literal["processing", "completed", "failed"] = "processing"


class ZoneResult(BaseModel):
    id: str
    label: str
    mean_deviation_mm: float
    max_deviation_mm: float
    action: Literal["REMOVE", "FILL", "KEEP"]
    severity: str
    tool: str
    grit: list[int]
    risk: str
    instructions: list[str]


class RepairStep(BaseModel):
    step: int
    title: str
    zones: list[str]
    tool: str
    grit: int
    instruction: str


class ComparisonResult(BaseModel):
    result_id: str
    scan_id: str
    reference_id: str
    scan_quality: dict
    reconstruction: dict
    summary: dict
    zones: list[ZoneResult]
    repair_plan: list[RepairStep]
    heatmap: list[dict]
