from app.database import products_collection, users_collection
from app.services.auth_service import serialize_user


async def get_dashboard_stats() -> dict:
    total_products = await products_collection.count_documents({})
    total_users = await users_collection.count_documents({"role": "user"})
    low_stock = await products_collection.count_documents({"stock": {"$lte": 5}})
    out_of_stock = await products_collection.count_documents({"stock": 0})


    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_value": {"$sum": {"$multiply": ["$price", "$stock"]}},
            }
        }
    ]
    
    agg = await products_collection.aggregate(pipeline).to_list(length=1)
    inventory_value = agg[0]["total_value"] if agg else 0

    categories = await products_collection.distinct("category")

    return {
        "total_products": total_products,
        "total_users": total_users,
        "low_stock": low_stock,
        "out_of_stock": out_of_stock,
        "inventory_value": round(inventory_value, 2),
        "total_categories": len(categories),
    }


async def list_users() -> list[dict]:
    return [serialize_user(u) async for u in users_collection.find({})]