from fastapi import HTTPException
from app.database import users_collection
from app.utils.security import hash_password, verify_password
from app.utils.jwt import create_access_token


async def register_user(user):
   
    existing_user = await users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "phone": user.phone,
        "address": user.address
    }

    result = await users_collection.insert_one(new_user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


async def login_user(user):
    
    db_user = await users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "id": str(db_user["_id"]),
            "email": db_user["email"],
            "name": db_user["name"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(db_user["_id"]),
            "name": db_user["name"],
            "email": db_user["email"],
            "phone": db_user.get("phone", ""),
            "address": db_user.get("address", "")
        }
    }