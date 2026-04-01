from app.database import db, redis
from app.models import document_model
from app.utils.hash import generate_hash
from app.services.redis_service import (
    get_user_jobs, increment_user_jobs,
    get_cached_summary
)
from fastapi import HTTPException

collection = db["documents"]

async def create_document(data):
    content_hash = generate_hash(data.content)

    cached = await get_cached_summary(content_hash)
    if cached:
        doc = document_model({
            "user_id": data.user_id,
            "title": data.title,
            "content": data.content,
            "content_hash": content_hash
        })
        doc["status"] = "completed"
        doc["summary"] = cached

        result = await collection.insert_one(doc)

        return {
            "document_id": str(result.inserted_id),
            "status": "completed",
            "summary": cached
        }

    jobs = await get_user_jobs(data.user_id)
    if jobs >= 3:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    await increment_user_jobs(data.user_id)

    doc = document_model({
        "user_id": data.user_id,
        "title": data.title,
        "content": data.content,
        "content_hash": content_hash
    })

    result = await collection.insert_one(doc)

    await redis.lpush("doc_queue", str(result.inserted_id))

    return {"document_id": str(result.inserted_id), "status": "queued"}