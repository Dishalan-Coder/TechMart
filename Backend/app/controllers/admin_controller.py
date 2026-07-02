from bson import ObjectId
from fastapi import HTTPException
from app.schemas.user_schema import ProductSchema

async def create_product(db, product: ProductSchema):
    product_dict = product.dict()
    product_dict["image_url"] = str(product_dict["image_url"]) # Store URL as string
    result = await db["products"].insert_one(product_dict)
    product_dict["id"] = str(result.inserted_id)
    return product_dict

async def update_product(db, product_id: str, product: ProductSchema):
    product_dict = product.dict()
    product_dict["image_url"] = str(product_dict["image_url"])
    
    result = await db["products"].update_one(
        {"_id": ObjectId(product_id)}, {"$set": product_dict}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found or no changes made")
    
    product_dict["id"] = product_id
    return product_dict

async def delete_product(db, product_id: str):
    result = await db["products"].delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}