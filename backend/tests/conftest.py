"""
Pytest fixtures shared across the test suite.
"""

import pytest
from fastapi.testclient import TestClient

from main import app
from app.services.storage import purge_all


@pytest.fixture(autouse=True)
def clean_uploads():
    """Wipe all uploads before and after each test."""
    purge_all()
    yield
    purge_all()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_pdf_bytes():
    """
    Minimal valid PDF bytes for upload validation tests.
    For real extraction tests, place a test PDF at tests/fixtures/sample.pdf
    """
    return b"%PDF-1.4 1 0 obj<</Type/Catalog>>endobj"
