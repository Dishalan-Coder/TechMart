from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field


class CartItemModel(BaseModel):
    product_id: str
    quantity: int = 1


class CartModel(BaseModel):
    """Representation of a cart document stored in MongoDB (one per user)."""

    user_id: str
    items: List[CartItemModel] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))