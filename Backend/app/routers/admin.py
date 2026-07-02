from fastapi import APIRouter, Depends
from app.controllers import admin_controller
from app.schemas.user_schema import UserResponse, UserUpdate, ProductResponse, ProductSchema
from app.dependencies import get_db, get_current_user 

admin_router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])

@admin_router.post("/products", response_model=ProductResponse)
async def add_product(product: ProductSchema, db=Depends(get_db)):
    return await admin_controller.create_product(db, product)

@admin_router.put("/products/{product_id}", response_model=ProductResponse)
async def edit_product(product_id: str, product: ProductSchema, db=Depends(get_db)):
    return await admin_controller.update_product(db, product_id, product)

@admin_router.delete("/products/{product_id}")
async def remove_product(product_id: str, db=Depends(get_db)):
    return await admin_controller.delete_product(db, product_id)