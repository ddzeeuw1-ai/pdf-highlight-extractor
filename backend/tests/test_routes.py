"""
Integration tests for API routes.
"""

import io


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_upload_valid_pdf(client, sample_pdf_bytes):
    r = client.post(
        "/api/upload",
        files={"file": ("test.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
    )
    assert r.status_code == 200
    data = r.json()
    assert "upload_id" in data
    assert data["filename"] == "test.pdf"


def test_upload_wrong_mime(client):
    r = client.post(
        "/api/upload",
        files={"file": ("test.txt", io.BytesIO(b"hello"), "text/plain")},
    )
    assert r.status_code == 415


def test_upload_not_a_pdf(client):
    r = client.post(
        "/api/upload",
        files={"file": ("fake.pdf", io.BytesIO(b"not a pdf"), "application/pdf")},
    )
    assert r.status_code == 422


def test_extract_not_found(client):
    r = client.post("/api/extract/nonexistent-id")
    assert r.status_code == 404


def test_export_invalid_format(client, sample_pdf_bytes):
    r = client.post(
        "/api/upload",
        files={"file": ("test.pdf", io.BytesIO(sample_pdf_bytes), "application/pdf")},
    )
    upload_id = r.json()["upload_id"]
    r2 = client.post(f"/api/export/{upload_id}?format=docx")
    assert r2.status_code == 400
