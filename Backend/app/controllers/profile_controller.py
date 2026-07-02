from ..database import users_collection
from fastapi import HTTPException


async def get_profile(user_id: str):
    user = await users_collection.find_one({"_id": user_id})

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["_id"] = str(user["_id"])
    return user



async def update_profile(user_id: str, data: dict):
    result = await users_collection.update_one(
        {"_id": user_id},
        {"$set": data}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")

    return {"message": "Profile updated successfully"}