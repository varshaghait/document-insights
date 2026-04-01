from fastapi import APIRouter
from app.database import db

router = APIRouter()
collection = db["documents"]

@router.get("/users/{user_id}/documents")
async def list_docs(user_id: str, status: str = None, page: int = 1, page_size: int = 10):
    query = {"user_id": user_id}

    if status:
        query["status"] = status

    skip = (page - 1) * page_size
    cursor = collection.find(query).skip(skip).limit(page_size)

    docs = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        docs.append(doc)

    return docs