from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.scan_routes import router as scan_router
from app.api.job_routes import router as job_router
from app.api.result_routes import router as result_router

app = FastAPI(title="TrueForm AI", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "product": "TrueForm AI"}


app.include_router(scan_router)
app.include_router(job_router)
app.include_router(result_router)
