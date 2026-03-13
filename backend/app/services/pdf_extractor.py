"""
PDF highlight extraction service.
Reads highlight annotations from a PDF file and extracts the underlying text
by matching annotation quad-point coordinates to the page's text layer.
"""

import warnings
from pathlib import Path

from pypdf import PdfReader
import pdfplumber

from app.services.text_cleaner import clean_text
from app.models.schemas import Highlight

warnings.filterwarnings("ignore")


def _get_annotation_quads(reader: PdfReader) -> list[dict]:
    """
    Iterate over all pages and collect highlight annotations with their
    quad-point bounding coordinates and page index.
    """
    annotations = []
    for page_num, page in enumerate(reader.pages):
        if "/Annots" not in page:
            continue
        for annot in page["/Annots"]:
            obj = annot.get_object()
            if obj.get("/Subtype") != "/Highlight":
                continue
            quads = obj.get("/QuadPoints")
            if quads:
                annotations.append({"page": page_num, "quads": list(quads)})

    # Sort: page order, then top-to-bottom on the page
    # PDF y=0 is at the bottom, so higher y value = higher on page
    annotations.sort(key=lambda a: (a["page"], -a["quads"][1]))
    return annotations


def _quads_to_bboxes(quads: list[float]) -> list[tuple[float, float, float, float]]:
    """
    Convert a flat list of QuadPoints (groups of 8 floats: 4 x/y corners)
    into a list of (x0, y0, x1, y1) bounding boxes.
    """
    bboxes = []
    for i in range(0, len(quads), 8):
        quad = quads[i : i + 8]
        xs = [quad[j] for j in range(0, 8, 2)]
        ys = [quad[j] for j in range(1, 8, 2)]
        bboxes.append((min(xs), min(ys), max(xs), max(ys)))
    return bboxes


def extract_highlights(pdf_path: Path) -> list[Highlight]:
    """
    Extract all highlighted text from a PDF file.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        List of Highlight objects, sorted by page and position.

    Raises:
        ValueError: If the file cannot be read or is not a valid PDF.
    """
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:
        raise ValueError(f"Could not read PDF: {exc}") from exc

    annotation_data = _get_annotation_quads(reader)

    if not annotation_data:
        return []

    results: list[Highlight] = []

    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for annotation in annotation_data:
                page_index = annotation["page"]
                page = pdf.pages[page_index]
                page_height = page.height

                bboxes = _quads_to_bboxes(annotation["quads"])
                word_parts: list[str] = []

                for x0, y0_pdf, x1, y1_pdf in bboxes:
                    # Convert from PDF bottom-origin coords to pdfplumber top-origin
                    top = page_height - y1_pdf
                    bottom = page_height - y0_pdf
                    crop = page.within_bbox(
                        (x0 - 2, top - 2, x1 + 2, bottom + 2),
                        strict=False,
                    )
                    word_parts.extend(w["text"] for w in crop.extract_words())

                raw_text = " ".join(word_parts)
                cleaned = clean_text(raw_text)

                if cleaned:
                    results.append(
                        Highlight(
                            page=page_index + 1,
                            text=cleaned,
                        )
                    )
    except Exception as exc:
        raise ValueError(f"Failed to extract text from PDF: {exc}") from exc

    return results
