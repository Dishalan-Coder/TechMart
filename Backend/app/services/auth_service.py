from datetime import timedelta

from fastapi import HTTPException, status

from app.config import settings
from app.database import users_collection
from app.models.user import UserModel
from app.schemas.auth import LoginRequest, RegisterRequest
from app.utils.jwt import create_access_token
from app.utils.security import hash_password, verify_password


def serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "user"),
        "phone": user.get("phone"),
        "address": user.get("address"),
    }


async def register_user(payload: RegisterRequest) -> dict:
    existing = await users_collection.find_one(
        {
            "email": payload.email.lower(),
        }
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists",
        )

    user = UserModel(
        name=payload.name,
        email=payload.email.lower(),
        hashed_password=hash_password(payload.password),
        role="user",
    )

    result = await users_collection.insert_one(
        user.model_dump()
    )

    created = await users_collection.find_one(
        {
            "_id": result.inserted_id,
        }
    )

    return build_token_response(created)


async def login_user(payload: LoginRequest) -> dict:
    user = await users_collection.find_one(
        {
            "email": payload.email.lower(),
        }
    )

    if (
        not user
        or not verify_password(
            payload.password,
            user["hashed_password"],
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return build_token_response(user)


def build_token_response(user: dict) -> dict:
    access_token = create_access_token(
        data={
            "sub": str(user["_id"]),
        },
        expires_delta=timedelta(
            minutes=settings.access_token_expire_minutes,
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": serialize_user(user),
    }