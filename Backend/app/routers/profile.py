from fastapi import APIRouter, Depends, status

from app.controllers import profile_controller
from app.dependencies import get_current_user
from app.schemas.user import (
    ChangePasswordRequest,
    UpdateProfileRequest,
    UserPublic,
)

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.put("", response_model=UserPublic)
async def update_profile(
    payload: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
):
    return await profile_controller.update_profile(
        current_user,
        payload,
    )


@router.put(
    "/password",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
):
    await profile_controller.change_password(
        current_user,
        payload,
    )