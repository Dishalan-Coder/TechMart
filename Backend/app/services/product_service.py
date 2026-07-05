from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

from app.database import products_collection
from app.models.product import ProductModel
from app.schemas.product import ProductCreateRequest, ProductUpdateRequest


def serialize_product(product: dict) -> dict:
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "category": product["category"],
        "brand": product.get("brand"),
        "stock": product.get("stock", 0),
        "image_url": product.get("image_url"),
        "rating": product.get("rating", 0.0),
    }


def _to_object_id(product_id: str) -> ObjectId:
    try:
        return ObjectId(product_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )


async def list_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = None,
):
    query = {}

    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    if category and category.lower() != "all":
        query["category"] = category

    if min_price is not None or max_price is not None:
        query["price"] = {}

        if min_price is not None:
            query["price"]["$gte"] = min_price

        if max_price is not None:
            query["price"]["$lte"] = max_price

    cursor = products_collection.find(query)

    sort_map = {
        "price_asc": [("price", 1)],
        "price_desc": [("price", -1)],
        "name_asc": [("name", 1)],
        "newest": [("created_at", -1)],
    }

    cursor = cursor.sort(sort_map.get(sort, [("created_at", -1)]))

    return [serialize_product(product) async for product in cursor]


async def get_product(product_id: str):
    oid = _to_object_id(product_id)

    product = await products_collection.find_one({"_id": oid})

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return serialize_product(product)


async def get_categories():
    return await products_collection.distinct("category")


async def create_product(payload: ProductCreateRequest):
    product = ProductModel(**payload.model_dump())

    result = await products_collection.insert_one(product.model_dump())

    created_product = await products_collection.find_one(
        {"_id": result.inserted_id}
    )

    return serialize_product(created_product)


async def update_product(product_id: str, payload: ProductUpdateRequest):
    oid = _to_object_id(product_id)

    updates = payload.model_dump(exclude_none=True)

    if updates:
        result = await products_collection.update_one(
            {"_id": oid},
            {"$set": updates},
        )

        if result.matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

    updated_product = await products_collection.find_one({"_id": oid})

    return serialize_product(updated_product)


async def delete_product(product_id: str):
    oid = _to_object_id(product_id)

    result = await products_collection.delete_one({"_id": oid})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )