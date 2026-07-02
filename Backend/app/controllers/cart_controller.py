from fastapi import APIRouter, Header, HTTPException
from bson import ObjectId

from app.database import cart_collection
from app.auth import verify_token

router = APIRouter(prefix="/cart", tags=["Cart"])



def get_user(authorization: str):
    if not authorization:
        raise HTTPException(401, "Token missing")

    token = authorization.replace("Bearer ", "")
    user = verify_token(token)

    if not user:
        raise HTTPException(401, "Invalid token")

    return user



@router.post("/add")
async def add_to_cart(item: dict, authorization: str = Header(None)):

    user = get_user(authorization)
    user_id = user["user_id"]

    existing = await cart_collection.find_one({
        "user_id": user_id,
        "product_id": item["product_id"]
    })

    if existing:
        await cart_collection.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": item.get("quantity", 1)}}
        )
        return {"message": "Cart updated"}

    await cart_collection.insert_one({
        "user_id": user_id,
        "product_id": item["product_id"],
        "quantity": item.get("quantity", 1)
    })

    return {"message": "Added to cart"}



@router.get("/")
async def get_cart(authorization: str = Header(None)):

    user = get_user(authorization)
    user_id = user["user_id"]

    cart = await cart_collection.find(
        {"user_id": user_id}
    ).to_list(100)

    for item in cart:
        item["_id"] = str(item["_id"])

    return cart


@router.delete("/{cart_id}")
async def delete_item(cart_id: str, authorization: str = Header(None)):

    user = get_user(authorization)
    user_id = user["user_id"]

    result = await cart_collection.delete_one({
        "_id": ObjectId(cart_id),
        "user_id": user_id
    })

    if result.deleted_count == 0:
        raise HTTPException(404, "Item not found")

    return {"message": "Deleted"}


@router.put("/{cart_id}")
async def update_quantity(cart_id: str, data: dict, authorization: str = Header(None)):

    user = get_user(authorization)
    user_id = user["user_id"]

    result = await cart_collection.update_one(
        {
            "_id": ObjectId(cart_id),
            "user_id": user_id
        },
        {
            "$set": {"quantity": data["quantity"]}
        }
    )

    if result.modified_count == 0:
        raise HTTPException(404, "Update failed")

    return {"message": "Quantity updated"}