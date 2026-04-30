import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import settings


ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_SIZE_BYTES = 5 * 1024 * 1024


def ensure_upload_dirs() -> None:
    Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)
    Path(settings.offer_letters_dir).mkdir(parents=True, exist_ok=True)


async def save_upload(file: UploadFile) -> str:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Only PDF and DOCX are supported.")
    data = await file.read()
    if len(data) > MAX_SIZE_BYTES:
        raise ValueError("File size exceeds 5MB limit.")
    ensure_upload_dirs()
    name = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(settings.uploads_dir, name)
    with open(path, "wb") as f:
        f.write(data)
    return path
