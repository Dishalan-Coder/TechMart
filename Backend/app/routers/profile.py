from fastapi import APIRouter, Depends
from ..controllers.profile_controller import get_profile, update_profile
from ..auth import get_current_user

router = APIRouter()


@router.get("/profile")
async def profile(user=Depends(get_current_user)):
    return await get_profile(user["user_id"])



@router.put("/profile")
async def update(user_data: dict, user=Depends(get_current_user)):
    return await update_profile(user["user_id"], user_data)