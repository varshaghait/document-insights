import asyncio
import random
from bson import ObjectId
from app.database import db, redis
from app.services.redis_service import decrement_user_jobs, cache_summary

collection = db["documents"]

async def worker():
    while True:
        job = await redis.brpop("doc_queue", timeout=5)

        if not job:
            await asyncio.sleep(1)
            continue

        doc_id = job[1]

        doc = await collection.find_one_and_update(
            {"_id": ObjectId(doc_id), "status": "queued"},
            {"$set": {"status": "processing"}},
            return_document=True
        )

        if not doc:
            continue

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