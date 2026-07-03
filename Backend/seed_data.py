import asyncio

from app.database import products_collection, users_collection
from app.models.product import ProductModel
from app.utils.security import hash_password


PRODUCTS = [
    dict(
        name="MCB Circuit Breaker 32A",
        description="Single pole miniature circuit breaker, 32A, C-curve, for residential distribution boards.",
        price=8.50,
        category="Circuit Protection",
        brand="Legrand",
        stock=120,
        image_url=None,
        rating=4.6,
    ),
    dict(
        name="LED Panel Light 18W",
        description="Slim recessed LED panel light, 18W, 6500K daylight, ideal for offices and homes.",
        price=12.99,
        category="Lighting",
        brand="Philips",
        stock=85,
        image_url=None,
        rating=4.4,
    ),
    dict(
        name="3-Core Copper Cable 2.5mm (100m)",
        description="Flexible 3-core copper wiring cable, 2.5mm sq, PVC insulated, 100m roll.",
        price=64.00,
        category="Wiring & Cables",
        brand="Polycab",
        stock=40,
        image_url=None,
        rating=4.7,
    ),
    dict(
        name="13A Switched Socket Outlet",
        description="Single gang 13A switched socket, white moulded, BS 1363 compliant.",
        price=3.25,
        category="Switches & Sockets",
        brand="MK Electric",
        stock=200,
        image_url=None,
        rating=4.5,
    ),
    dict(
        name="Digital Clamp Meter",
        description="Auto-ranging digital clamp meter for AC/DC current, voltage, resistance and continuity testing.",
        price=39.90,
        category="Tools & Testers",
        brand="Fluke",
        stock=25,
        image_url=None,
        rating=4.8,
    ),
    dict(
        name="Ceiling Fan with Remote 52-inch",
        description="Energy efficient 52-inch ceiling fan with 3-speed remote control.",
        price=54.00,
        category="Appliances",
        brand="Havells",
        stock=30,
        image_url=None,
        rating=4.3,
    ),
    dict(
        name="RCD Residual Current Device 40A",
        description="2-pole RCD, 40A, 30mA trip sensitivity, for earth leakage protection.",
        price=15.75,
        category="Circuit Protection",
        brand="Schneider Electric",
        stock=60,
        image_url=None,
        rating=4.6,
    ),
    dict(
        name="Extension Cord 4-Socket 5m",
        description="Heavy duty extension lead with 4 sockets, surge protection, 5 metre cable.",
        price=11.20,
        category="Wiring & Cables",
        brand="Belkin",
        stock=150,
        image_url=None,
        rating=4.2,
    ),
    dict(
        name="LED Bulb 9W B22 Pack of 4",
        description="Energy saving LED bulbs, 9W, bayonet B22 fitting, warm white, pack of 4.",
        price=7.99,
        category="Lighting",
        brand="Osram",
        stock=300,
        image_url=None,
        rating=4.5,
    ),
    dict(
        name="Distribution Board 8-Way",
        description="8-way consumer unit distribution board with metal enclosure, ready for MCB installation.",
        price=42.50,
        category="Circuit Protection",
        brand="Hager",
        stock=18,
        image_url=None,
        rating=4.4,
    ),
    dict(
        name="Dimmer Switch Single Gang",
        description="Rotary dimmer switch for dimmable LED and incandescent lighting circuits.",
        price=9.40,
        category="Switches & Sockets",
        brand="MK Electric",
        stock=90,
        image_url=None,
        rating=4.1,
    ),
    dict(
        name="Soldering Iron Kit 60W",
        description="60W adjustable temperature soldering iron kit with stand and accessories.",
        price=22.30,
        category="Tools & Testers",
        brand="Weller",
        stock=45,
        image_url=None,
        rating=4.6,
    ),
]


async def seed():
    existing = await products_collection.count_documents({})

    if existing == 0:
        docs = [
            ProductModel(**product).model_dump()
            for product in PRODUCTS
        ]

        await products_collection.insert_many(docs)

        print(f"Inserted {len(docs)} products.")
    else:
        print(
            f"Products collection already has {existing} documents, "
            "skipping product seed."
        )

    admin_email = "admin@techmart.com"

    admin = await users_collection.find_one(
        {
            "email": admin_email,
        }
    )

    if not admin:
        await users_collection.insert_one(
            {
                "name": "Admin",
                "email": admin_email,
                "hashed_password": hash_password("Admin@123"),
                "phone": None,
                "address": None,
                "role": "admin",
            }
        )

        print(
            f"Created admin account: {admin_email} / Admin@123"
        )
    else:
        print("Admin account already exists.")


if __name__ == "__main__":
    asyncio.run(seed())