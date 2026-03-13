"""
Temporary file storage for uploaded PDFs.
Files are stored with a UUID-based name and auto-deleted after a configurable TTL.
"""

import asyncio
import shutil
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from config import settings

# In-memory registry: upload_id -> (path, expires_at)
_registry: dict[str, tuple[Path, datetime]] = {}


def _upload_dir() -> Path:
    path = Path(settings.upload_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_upload(data: bytes, original_filename: str) -> str:
    """
    Save uploaded PDF bytes to a temp file.
    Returns a unique upload_id.
    """
    upload_id = str(uuid.uuid4())
    suffix = Path(original_filename).suffix or ".pdf"
    dest = _upload_dir() / f"{upload_id}{suffix}"
    dest.write_bytes(data)

    expires_at = datetime.utcnow() + timedelta(seconds=settings.upload_ttl_seconds)
    _registry[upload_id] = (dest, expires_at)
    return upload_id


def get_upload_path(upload_id: str) -> Path:
    """
    Return the Path for a given upload_id, or raise KeyError if not found / expired.
    """
    if upload_id not in _registry:
        raise KeyError(f"Upload not found: {upload_id}")
    path, expires_at = _registry[upload_id]
    if datetime.utcnow() > expires_at:
        _delete(upload_id)
        raise KeyError(f"Upload expired: {upload_id}")
    return path


def _delete(upload_id: str) -> None:
    entry = _registry.pop(upload_id, None)
    if entry:
        path, _ = entry
        path.unlink(missing_ok=True)


async def cleanup_loop() -> None:
    """Background coroutine that deletes expired uploads every 5 minutes."""
    while True:
        await asyncio.sleep(300)
        now = datetime.utcnow()
        expired = [uid for uid, (_, exp) in _registry.items() if now > exp]
        for uid in expired:
            _delete(uid)


def purge_all() -> None:
    """Delete all uploads (used in tests)."""
    for uid in list(_registry.keys()):
        _delete(uid)
    upload_path = Path(settings.upload_dir)
    if upload_path.exists():
        shutil.rmtree(upload_path)
