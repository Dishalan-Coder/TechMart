from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings


client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.database_name]

users_collection = database["users"]
products_collection = database["products"]
carts_collection = database["carts"]


async def init_indexes():
    await users_collection.create_index("email", unique=True)
    await products_collection.create_index("name")
    await products_collection.create_index("category")
    await carts_collection.create_index("user_id", unique=True)


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_indexes())