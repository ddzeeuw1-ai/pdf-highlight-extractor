"""
POST /api/extract  — Extract highlights from a previously uploaded PDF.
"""

from fastapi import APIRouter, HTTPException

from app.models.schemas import ExtractResponse
from app.services import storage
from app.services.pdf_extractor import extract_highlights

router = APIRouter()


@router.post("/extract/{upload_id}", response_model=ExtractResponse)
async def extract(upload_id: str) -> ExtractResponse:
    """
    Extract all highlighted text from an uploaded PDF.

    - **upload_id**: The ID returned by POST /api/upload
    """
    try:
        pdf_path = storage.get_upload_path(upload_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    try:
        highlights = extract_highlights(pdf_path)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return ExtractResponse(
        upload_id=upload_id,
        filename=pdf_path.name,
        total=len(highlights),
        highlights=highlights,
    )
