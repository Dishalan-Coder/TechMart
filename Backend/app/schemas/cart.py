from pydantic import BaseModel


class CartItemRequest(BaseModel):
    product_id: str
    quantity: int = 1


class UpdateCartItemRequest(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    product_id: str
    quantity: int
    name: str
    price: float
    image_url: str | None = None
    stock: int


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total: float