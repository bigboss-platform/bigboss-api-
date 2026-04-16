import uuid
from pathlib import Path

from fastapi import UploadFile

from app.core.config import settings

MEDIA_ROOT = Path("media")


async def save_upload_file(file: UploadFile, subdirectory: str) -> str:
    destination = MEDIA_ROOT / subdirectory
    destination.mkdir(parents=True, exist_ok=True)
    extension = Path(file.filename or "file").suffix
    filename = f"{uuid.uuid4()}{extension}"
    file_path = destination / filename
    contents = await file.read()
    file_path.write_bytes(contents)
    return f"{settings.media_base_url}/{subdirectory}/{filename}"
