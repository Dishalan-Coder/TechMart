from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from prefect import flow, task, get_run_logger


client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.Tech_Mart]

users_collection = database["users"]
products_collection = database["products"]
carts_collection = database["carts"]


