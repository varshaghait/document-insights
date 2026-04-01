import asyncio
import random
from app.database import db
from app.services.redis_service import decrement_user_jobs, cache_summary

collection = db["documents"]

async def worker():
    while True:
        doc = await collection.find_one({"status": "queued"})
        if not doc:
            await asyncio.sleep(2)
            continue

        await collection.update_one(
            {"_id": doc["_id"]},
            {"$set": {"status": "processing"}}
        )

        await asyncio.sleep(random.randint(10, 20))

        if random.random() < 0.1:
            await collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"status": "failed"}}
            )
        else:
            summary = f"Summary of: {doc['title']}"
            await collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"status": "completed", "summary": summary}}
            )

            await cache_summary(doc["content_hash"], summary)

        await decrement_user_jobs(doc["user_id"])