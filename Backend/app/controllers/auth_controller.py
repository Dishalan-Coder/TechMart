from app.schemas.auth import LoginRequest, RegisterRequest
from app.services import auth_service


async def register(payload: RegisterRequest) -> dict:
    return await auth_service.register_user(payload)


async def login(payload: LoginRequest) -> dict:
    return await auth_service.login_user(payload)