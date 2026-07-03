from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

from app.database import carts_collection, products_collection
from app.schemas.cart import CartItemRequest


async def _get_or_create_cart(user_id: str) -> dict:
    cart = await carts_collection.find_one({"user_id": user_id})
    if not cart:
        await carts_collection.insert_one({"user_id": user_id, "items": []})
        cart = await carts_collection.find_one({"user_id": user_id})
    return cart


async def _build_cart_response(cart: dict) -> dict:
    items_response = []
    total = 0.0
    for item in cart.get("items", []):
        try:
            oid = ObjectId(item["product_id"])
        except InvalidId:
            continue
        product = await products_collection.find_one({"_id": oid})
        if not product:
            continue
        line_total = product["price"] * item["quantity"]
        total += line_total
        items_response.append(
            {
                "product_id": item["product_id"],
                "quantity": item["quantity"],
                "name": product["name"],
                "price": product["price"],
                "image_url": product.get("image_url"),
                "stock": product.get("stock", 0),
            }
        )
    return {"items": items_response, "total": round(total, 2)}


async def get_cart(user_id: str) -> dict:
    cart = await _get_or_create_cart(user_id)
    return await _build_cart_response(cart)


async def add_to_cart(user_id: str, payload: CartItemRequest) -> dict:
    try:
        oid = ObjectId(payload.product_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = await products_collection.find_one({"_id": oid})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    cart = await _get_or_create_cart(user_id)
    items = cart.get("items", [])
    existing = next((i for i in items if i["product_id"] == payload.product_id), None)

    if existing:
        new_qty = existing["quantity"] + payload.quantity
    else:
        new_qty = payload.quantity

    if new_qty > product.get("stock", 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.get('stock', 0)} units of '{product['name']}' available",
        )

    if existing:
        await carts_collection.update_one(
            {"user_id": user_id, "items.product_id": payload.product_id},
            {"$set": {"items.$.quantity": new_qty}},
        )
    else:
        await carts_collection.update_one(
            {"user_id": user_id},
            {"$push": {"items": {"product_id": payload.product_id, "quantity": payload.quantity}}},
        )

    updated_cart = await carts_collection.find_one({"user_id": user_id})
    return await _build_cart_response(updated_cart)


async def update_cart_item(user_id: str, product_id: str, quantity: int) -> dict:
    if quantity <= 0:
        return await remove_from_cart(user_id, product_id)

    try:
        oid = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product = await products_collection.find_one({"_id": oid})
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if quantity > product.get("stock", 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Only {product.get('stock', 0)} units of '{product['name']}' available",
        )

    result = await carts_collection.update_one(
        {"user_id": user_id, "items.product_id": product_id},
        {"$set": {"items.$.quantity": quantity}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")

    updated_cart = await carts_collection.find_one({"user_id": user_id})
    return await _build_cart_response(updated_cart)


async def remove_from_cart(user_id: str, product_id: str) -> dict:
    await carts_collection.update_one(
        {"user_id": user_id}, {"$pull": {"items": {"product_id": product_id}}}
    )
    updated_cart = await carts_collection.find_one({"user_id": user_id})
    return await _build_cart_response(updated_cart)


async def clear_cart(user_id: str) -> dict:
    await carts_collection.update_one({"user_id": user_id}, {"$set": {"items": []}})
    updated_cart = await carts_collection.find_one({"user_id": user_id})
    return await _build_cart_response(updated_cart)