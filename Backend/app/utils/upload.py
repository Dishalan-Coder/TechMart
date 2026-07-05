import os
import uuid

from fastapi import UploadFile

from app.config import settings

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def save_upload_file(file: UploadFile) -> str:
    """Saves an uploaded image to disk and returns a relative URL path."""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = ".jpg"

    os.makedirs(settings.upload_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(settings.upload_dir, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    return f"/uploads/{filename}"