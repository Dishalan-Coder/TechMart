from pydantic import BaseModel, Field


class ProductPublic(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    brand: str | None = None
    stock: int
    image_url: str | None = None
    rating: float = 0.0


class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    category: str = Field(..., min_length=1)
    brand: str | None = None
    stock: int = Field(default=0, ge=0)
    image_url: str | None = None


class ProductUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    category: str | None = None
    brand: str | None = None
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None