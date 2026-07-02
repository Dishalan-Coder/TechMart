from fastapi import APIRouter, HTTPException
from ..schemas import UserCreate, UserLogin
from ..database import users_collection
from ..security import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register(user: UserCreate):

    
    existing_user = await users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    
    new_user = {
        "full_name": user.full_name,
        "email": user.email,
        "password": hash_password(user.password)
    }

    
    result = await users_collection.insert_one(new_user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }


@router.post("/login")
async def login(user: UserLogin):

    
    existing_user = await users_collection.find_one(
        {"email": user.email}
    )

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    
    if not verify_password(
        user.password,
        existing_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user": {
            "id": str(existing_user["_id"]),
            "full_name": existing_user["full_name"],
            "email": existing_user["email"]
        }
    }