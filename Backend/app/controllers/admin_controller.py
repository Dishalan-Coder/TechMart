from app.services import admin_service


async def get_dashboard_stats() -> dict:
    return await admin_service.get_dashboard_stats()


async def list_users() -> list[dict]:
    return await admin_service.list_users()