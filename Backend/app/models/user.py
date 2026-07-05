from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    """Representation of a user document stored in MongoDB."""

    name: str
    email: EmailStr
    hashed_password: str
    phone: Optional[str] = None
    address: Optional[str] = None
    role: str = "user"  # "user" or "admin"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))