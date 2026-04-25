# SandingGuide AI (MVP)

Scan → Understand → Decide → Act

A practical MVP that compares a scanned object vs a reference geometry/spec, computes deviations, classifies zones into REMOVE/FILL/KEEP, and produces action-focused guidance plus exportable reports.

## Stack

- **Frontend:** Next.js, React, TypeScript, TailwindCSS, React Three Fiber
- **Backend:** FastAPI, NumPy, Trimesh, Open3D, Pydantic

## Repository structure

```text
backend/
  api/
  core/
  geometry/
  logic/
  output/
  data/sample/
frontend/
  app/
  components/
  lib/
```

## Features implemented

- Upload scan/reference files (`.ply`, `.obj`, `.stl`, `.glb`, `.usdz`*)
- Reference options:
  - Mesh file
  - JSON spec
  - Simple dimensions form (backend API support)
- Pipeline:
  1. Load + optional scale normalization
  2. Convert mesh → point cloud
  3. ICP alignment (Open3D)
  4. Per-point signed deviation
  5. Zone segmentation
  6. Zone decision (REMOVE/FILL/KEEP)
  7. Sanding/filling recommendations
  8. Risk + scan quality feedback
  9. Structured outputs + JSON/PDF report generation
- Interactive 3D zone heatmap viewer (color-coded action overlay)
- Step-by-step action plan
- JSON report download and PDF output path

> *USDZ support depends on Trimesh converter support in your local environment.

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data/sample/generate_sample_data.py
uvicorn main:app --reload --port 8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend expects backend at:

```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000/api
```

## API docs

FastAPI Swagger:

- `http://localhost:8000/docs`

### Endpoints

- `POST /api/upload`
- `POST /api/compare`
- `GET /api/result/{job_id}`
- `GET /api/health`

### `/api/compare` form fields

- `scan_file` (string, required)
- `reference_file` (string, optional)
- `reference_spec_json` (JSON string, optional)
- `dimension_reference_json` (JSON string, optional)

## JSON reference format

```json
{
  "object_name": "example",
  "units": "mm",
  "tolerance_mm": 0.2,
  "known_scale": {
    "dimension": "width",
    "value": 120
  },
  "zones": [
    {
      "id": "top_surface",
      "type": "flat",
      "target": "match_reference",
      "max_allowed_excess_mm": 0.2
    }
  ]
}
```

## Sample data

Generate sample data:

```bash
cd backend
python data/sample/generate_sample_data.py
```

Files created in `backend/data/sample`:

- `cube_reference.stl`
- `cube_scan_deformed.stl`
- `reference_spec.json`

## Usage flow

1. Open Upload page.
2. Upload deformed scan + reference mesh.
3. System runs full compare pipeline.
4. Open Viewer for zone heatmap + per-zone action/tool/grit.
5. Open Report for scan quality + action steps + exports.

## TODO (next iterations)

- Robust USDZ conversion pipeline with explicit converter fallback
- Better segmentation (feature-aware zones vs grid bins)
- True mesh overlay split view with synchronized cameras
- More robust signed distance computation (surface normals / SDF)
- Persistent job storage and report file download endpoint
- Additional material-specific sanding/filling rule profiles
- Progress streaming for long-running jobs

