"""
PDF Highlight Extractor — FastAPI application entry point.
"""

import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import upload, extract, export
from app.services.storage import cleanup_loop
from config import settings

app = FastAPI(
    title="PDF Highlight Extractor",
    description=(
        "Extract highlighted text from PDF files. "
        "Upload a PDF, extract its highlights, and download the results "
        "as plain text, Markdown, or JSON."
    ),
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# ── CORS ──────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(extract.router, prefix="/api", tags=["Extract"])
app.include_router(export.router, prefix="/api", tags=["Export"])


# ── Startup / shutdown ────────────────────────────────────────
@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(cleanup_loop())


@app.get("/api/health", tags=["Health"])
async def health() -> dict:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=settings.debug)
