"""
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field


class Highlight(BaseModel):
    """A single extracted highlight from a PDF."""
    page: int = Field(..., description="1-based page number")
    text: str = Field(..., description="Cleaned extracted text of the highlight")


class UploadResponse(BaseModel):
    """Returned after a successful PDF upload."""
    upload_id: str
    filename: str
    size_bytes: int


class ExtractResponse(BaseModel):
    """Returned after highlight extraction completes."""
    upload_id: str
    filename: str
    total: int = Field(..., description="Number of highlights found")
    highlights: list[Highlight]


class ErrorResponse(BaseModel):
    """Returned when an error occurs."""
    detail: str
