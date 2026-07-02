from fastapi import APIRouter, Depends

from app.controllers import admin_controller
from app.dependencies import get_current_admin
from app.schemas.user import UserPublic

router = APIRouter(
    prefix="/api/admin", 
    tags=["Admin"], 
    dependencies=[Depends(get_current_admin)]
)


@router.get("/stats")
async def get_dashboard_stats():
    return await admin_controller.get_dashboard_stats()


@router.get("/users", response_model=list[UserPublic])
async def list_users():
    return await admin_controller.list_users()