import os
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

MONGO_URL = os.getenv("MONGO_URL")
REDIS_URL = os.getenv("REDIS_URL")

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["doc_db"]

redis = Redis.from_url(REDIS_URL, decode_responses=True)