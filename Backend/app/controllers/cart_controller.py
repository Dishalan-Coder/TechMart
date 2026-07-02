from app.schemas.cart import CartItemRequest
from app.services import cart_service


async def get_cart(user_id: str) -> dict:
    return await cart_service.get_cart(user_id)


async def add_to_cart(user_id: str, payload: CartItemRequest) -> dict:
    return await cart_service.add_to_cart(user_id, payload)


async def update_cart_item(user_id: str, product_id: str, quantity: int) -> dict:
    return await cart_service.update_cart_item(user_id, product_id, quantity)


async def remove_from_cart(user_id: str, product_id: str) -> dict:
    return await cart_service.remove_from_cart(user_id, product_id)


async def clear_cart(user_id: str) -> dict:
    return await cart_service.clear_cart(user_id)