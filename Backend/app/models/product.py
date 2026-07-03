from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    """Representation of a product document stored in MongoDB."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)

    brand: Optional[str] = None
    stock: int = Field(default=0, ge=0)
    image_url: Optional[str] = None
    rating: float = Field(default=0.0, ge=0, le=5)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )