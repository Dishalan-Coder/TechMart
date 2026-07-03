from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from prefect import flow, task, get_run_logger


client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_uri)
database = client[settings.Tech_Mart]

users_collection = database["users"]
products_collection = database["products"]
carts_collection = database["carts"]


@task(name="Create MongoDB Indexes", description="Ensures required indexes exist in the database.")
async def init_indexes():
    
    logger = get_run_logger()
    logger.info("Starting database index creation...")
    
    await users_collection.create_index("email", unique=True)
    await products_collection.create_index("name")
    await products_collection.create_index("category")
    await carts_collection.create_index("user_id", unique=True)
    
    logger.info("Database indexes created successfully!")


@flow(name="Database Initialization Flow")
async def db_setup_flow():
    """Main flow to handle database setup tasks."""
   
    await init_indexes()


if __name__ == "__main__":
    import asyncio
   
    asyncio.run(db_setup_flow())