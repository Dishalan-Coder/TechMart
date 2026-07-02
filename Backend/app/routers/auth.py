from fastapi import APIRouter, status

from app.controllers import auth_controller
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest):
    return await auth_controller.register(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    return await auth_controller.login(payload)