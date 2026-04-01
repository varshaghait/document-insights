import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["document_insights"]

redis = Redis.from_url(REDIS_URL, decode_responses=True)

async def create_indexes():
    await db["documents"].create_index("content_hash")
    await db["documents"].create_index("user_id")
    await db["documents"].create_index("status")

async def check_connections():
    await redis.ping()
    await db.command("ping")