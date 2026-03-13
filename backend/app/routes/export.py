"""
POST /api/export  — Format and download highlights as txt, markdown, or json.
"""

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.models.schemas import Highlight
from app.services import storage
from app.services.pdf_extractor import extract_highlights

router = APIRouter()

FORMATS = ("txt", "markdown", "json")


def _to_txt(filename: str, highlights: list[Highlight]) -> str:
    title = f"Highlights — {Path(filename).stem}"
    lines = [title, "=" * len(title), "", f"Total highlights: {len(highlights)}", "", "=" * 60, ""]
    for i, h in enumerate(highlights, 1):
        lines += [f"[{i}] Page {h.page}", h.text, ""]
    return "\n".join(lines)


def _to_markdown(filename: str, highlights: list[Highlight]) -> str:
    stem = Path(filename).stem
    lines = [f"# Highlights — {stem}", "", f"**Total highlights:** {len(highlights)}", "", "---", ""]
    for i, h in enumerate(highlights, 1):
        lines += [f"## [{i}] Page {h.page}", "", h.text, ""]
    return "\n".join(lines)


def _to_json(highlights: list[Highlight]) -> str:
    return json.dumps([h.model_dump() for h in highlights], indent=2, ensure_ascii=False)


@router.post("/export/{upload_id}")
async def export_highlights(upload_id: str, format: str = "txt") -> Response:
    """
    Extract highlights from an uploaded PDF and return them as a downloadable file.

    - **upload_id**: The ID returned by POST /api/upload
    - **format**: One of `txt`, `markdown`, `json` (default: `txt`)
    """
    if format not in FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid format '{format}'. Choose one of: {', '.join(FORMATS)}",
        )

    try:
        pdf_path = storage.get_upload_path(upload_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    try:
        highlights = extract_highlights(pdf_path)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    stem = pdf_path.stem

    if format == "txt":
        content = _to_txt(pdf_path.name, highlights)
        media_type = "text/plain"
        download_name = f"{stem} - Highlights.txt"
    elif format == "markdown":
        content = _to_markdown(pdf_path.name, highlights)
        media_type = "text/markdown"
        download_name = f"{stem} - Highlights.md"
    else:  # json
        content = _to_json(highlights)
        media_type = "application/json"
        download_name = f"{stem} - Highlights.json"

    return Response(
        content=content.encode("utf-8"),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{download_name}"'},
    )
