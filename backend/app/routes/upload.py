"""
POST /api/upload  — Accept a PDF file and store it temporarily.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File

from app.models.schemas import UploadResponse
from app.services import storage
from config import settings

router = APIRouter()

ALLOWED_MIME_TYPES = {"application/pdf"}
PDF_MAGIC_BYTES = b"%PDF"


@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)) -> UploadResponse:
    """
    Upload a PDF file for highlight extraction.
    The file is stored temporarily and auto-deleted after the configured TTL.
    """
    # Validate content type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Only PDF files are accepted. Got: {file.content_type}",
        )

    data = await file.read()

    # Validate file size
    if len(data) > settings.max_upload_bytes:
        mb = settings.max_upload_bytes // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {mb} MB.",
        )

    # Validate PDF magic bytes (first 4 bytes must be %PDF)
    if not data.startswith(PDF_MAGIC_BYTES):
        raise HTTPException(
            status_code=422,
            detail="The uploaded file does not appear to be a valid PDF.",
        )

    upload_id = storage.save_upload(data, file.filename or "upload.pdf")

    return UploadResponse(
        upload_id=upload_id,
        filename=file.filename or "upload.pdf",
        size_bytes=len(data),
    )
