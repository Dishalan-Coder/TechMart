from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
)
from pydantic import BaseModel

from app.controllers import product_controller
from app.dependencies import get_current_admin
from app.schemas.product import (
    ProductCreateRequest,
    ProductPublic,
    ProductUpdateRequest,
)
from app.utils.upload import save_upload_file


router = APIRouter(
    prefix="/api/products",
    tags=["Products"],
)


class UploadResponse(BaseModel):
    url: str

@router.get("", response_model=list[ProductPublic])
async def list_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = None,
):
    return await product_controller.list_products(
        search,
        category,
        min_price,
        max_price,
        sort,
    )

@router.get("/categories", response_model=list[str])
async def get_categories():
    return await product_controller.get_categories()

@router.get("/{product_id}", response_model=ProductPublic)
async def get_product(product_id: str):
    return await product_controller.get_product(product_id)


@router.post(
    "",
    response_model=ProductPublic,
    dependencies=[Depends(get_current_admin)],
)
async def create_product(payload: ProductCreateRequest):
    return await product_controller.create_product(payload)


@router.put(
    "/{product_id}",
    response_model=ProductPublic,
    dependencies=[Depends(get_current_admin)],
)
async def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
):
    return await product_controller.update_product(
        product_id,
        payload,
    )


@router.delete(
    "/{product_id}",
    status_code=204,
    dependencies=[Depends(get_current_admin)],
)
async def delete_product(product_id: str):
    await product_controller.delete_product(product_id)

@router.post(
    "/upload-image",
    response_model=UploadResponse,
    dependencies=[Depends(get_current_admin)],
)
async def upload_image(
    file: UploadFile = File(...),
):
    url = save_upload_file(file)
    return {"url": url}