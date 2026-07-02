from app.services.auth_service import serialize_user


async def get_me(user: dict) -> dict:
    return serialize_user(user)