from fastapi import APIRouter, Depends

from app.controllers import user_controller
from app.dependencies import get_current_user
from app.schemas.user import UserPublic

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.get("/me", response_model=UserPublic)
async def get_me(current_user: dict = Depends(get_current_user)):
    return await user_controller.get_me(current_user)