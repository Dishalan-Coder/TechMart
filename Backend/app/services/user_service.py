from bson import ObjectId
from fastapi import HTTPException, status

from app.database import users_collection
from app.schemas.user import (
    ChangePasswordRequest,
    UpdateProfileRequest,
)
from app.services.auth_service import serialize_user
from app.utils.security import (
    hash_password,
    verify_password,
)


async def update_profile(
    user: dict,
    payload: UpdateProfileRequest,
) -> dict:
    updates = {
        k: v
        for k, v in payload.model_dump().items()
        if v is not None
    }

    if updates:
        await users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": updates},
        )

    updated = await users_collection.find_one(
        {"_id": user["_id"]}
    )

    return serialize_user(updated)


async def change_password(
    user: dict,
    payload: ChangePasswordRequest,
) -> None:
    if not verify_password(
        payload.current_password,
        user["hashed_password"],
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    new_hashed = hash_password(payload.new_password)

    await users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {
                "hashed_password": new_hashed,
            }
        },
    )