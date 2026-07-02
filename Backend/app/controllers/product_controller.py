from typing import Optional

from app.schemas.product import ProductCreateRequest, ProductUpdateRequest
from app.services import product_service


async def list_products(
    search: Optional[str], category: Optional[str], min_price: Optional[float],
    max_price: Optional[float], sort: Optional[str],
) -> list[dict]:
    return await product_service.list_products(search, category, min_price, max_price, sort)


async def get_product(product_id: str) -> dict:
    return await product_service.get_product(product_id)


async def get_categories() -> list[str]:
    return await product_service.get_categories()


async def create_product(payload: ProductCreateRequest) -> dict:
    return await product_service.create_product(payload)


async def update_product(product_id: str, payload: ProductUpdateRequest) -> dict:
    return await product_service.update_product(product_id, payload)


async def delete_product(product_id: str) -> None:
    await product_service.delete_product(product_id)