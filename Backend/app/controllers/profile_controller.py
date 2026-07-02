from app.schemas.user import ChangePasswordRequest, UpdateProfileRequest
from app.services import user_service


async def update_profile(user: dict, payload: UpdateProfileRequest) -> dict:
    return await user_service.update_profile(user, payload)


async def change_password(user: dict, payload: ChangePasswordRequest) -> None:
    await user_service.change_password(user, payload)