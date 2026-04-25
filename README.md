# TrueForm AI (Mobile Web MVP)

**Scan any object. Find the flaws. Get the exact fix plan.**

TrueForm AI is a physical object correction platform. It starts with a phone camera scan, builds a reconstruction (mock by default, COLMAP optional), compares against a target/reference, and returns a **Flaw Map**, **Deviation Map**, and **Fix Plan** with action guidance: **Remove / Fill / Keep / Rescan / Verify**.

## Product flow

1. Open app on phone and tap **Start Scan**
2. Allow camera access
3. Capture frames while moving around object
4. Review scan quality feedback
5. Process scan (mock reconstruction by default)
6. Add reference (mesh / JSON / dimensions)
7. Compare and get Flaw Map + Deviation Summary + Fix Plan
8. Download flaw correction report (JSON/PDF)

## Architecture

```text
backend/
  app/
    main.py
    api/
      scan_routes.py
      job_routes.py
      result_routes.py
    services/
      scan_session_service.py
      frame_quality_service.py
      reconstruction_service.py
      comparison_service.py
      report_service.py
      job_service.py
    providers/
      base_reconstruction_provider.py
      mock_reconstruction_provider.py
      colmap_reconstruction_provider.py
    geometry/
      align.py
      deviation.py
      segmentation.py
      mesh_utils.py
    logic/
      action_classifier.py
      repair_plan.py
      sanding_rules.py
      filling_rules.py
      risk_engine.py
    models/
      schemas.py
    storage/
      file_store.py
frontend/
  app/
    /
    /scan
    /scan/review/[scanId]
    /reference/[scanId]
    /processing/[jobId]
    /result/[jobId]
```

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

If backend runs elsewhere:

```bash
NEXT_PUBLIC_API_BASE=http://localhost:8000/api
```

## Phone testing notes

- Camera API requires HTTPS on phone (except localhost).
- A phone cannot use laptop localhost directly unless tunneled.
- Use Vercel + backend host, or HTTPS tunnel (ngrok/cloudflared).

## API endpoints

- `GET /api/health`
- `POST /api/scan/start`
- `POST /api/scan/{scan_id}/frame`
- `POST /api/scan/{scan_id}/finish`
- `POST /api/scan/{scan_id}/process`
- `GET /api/job/{job_id}/status`
- `POST /api/job/{job_id}/reference`
- `POST /api/job/{job_id}/compare`
- `GET /api/result/{result_id}`
- `GET /api/result/{result_id}/report.json`
- `GET /api/result/{result_id}/report.pdf`

## Reconstruction provider behavior

### Mock provider (default)
- Always available.
- Creates synthetic mesh so MVP remains functional.
- Result includes warning that demo reconstruction was used.

### COLMAP provider (optional)
Set env:

```bash
export TRUEFORM_RECON_PROVIDER=colmap
export TRUEFORM_DEV_FALLBACK=1
```

- If COLMAP is installed, provider attempts automatic reconstruction.
- If COLMAP is missing/fails and fallback is enabled, app falls back to mock with warning.
- If fallback is disabled, process returns an error.

## Current MVP scope

- Mobile-first scan capture with `getUserMedia` rear camera request.
- Frame upload and quality checks (blur, brightness, resolution signals).
- Session quality scoring: LOW / MEDIUM / GOOD.
- Reference by mesh/JSON/dimensions.
- Deviation-based zone classification and correction plan generation.
- 3D heatmap viewer and downloadable report.

