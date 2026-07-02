from fastapi import APIRouter, Depends

from app.controllers import cart_controller
from app.dependencies import get_current_user
from app.schemas.cart import CartItemRequest, CartResponse, UpdateCartItemRequest

router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.get("", response_model=CartResponse)
async def get_cart(current_user: dict = Depends(get_current_user)):
    return await cart_controller.get_cart(str(current_user["_id"]))


@router.post("", response_model=CartResponse)
async def add_to_cart(payload: CartItemRequest, current_user: dict = Depends(get_current_user)):
    return await cart_controller.add_to_cart(str(current_user["_id"]), payload)


@router.put("/{product_id}", response_model=CartResponse)
async def update_cart_item(
    product_id: str, payload: UpdateCartItemRequest, current_user: dict = Depends(get_current_user)
):
    return await cart_controller.update_cart_item(str(current_user["_id"]), product_id, payload.quantity)


@router.delete("/{product_id}", response_model=CartResponse)
async def remove_from_cart(product_id: str, current_user: dict = Depends(get_current_user)):
    return await cart_controller.remove_from_cart(str(current_user["_id"]), product_id)


@router.delete("", response_model=CartResponse)
async def clear_cart(current_user: dict = Depends(get_current_user)):
    return await cart_controller.clear_cart(str(current_user["_id"]))