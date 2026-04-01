from fastapi import APIRouter
from app.schemas import DocumentCreate
from app.services.document_service import create_document
from app.database import db
from bson import ObjectId
from fastapi import HTTPException

router = APIRouter()
collection = db["documents"]

@router.post("/documents")
async def create_doc(doc: DocumentCreate):
    return await create_document(doc)

from fastapi import HTTPException

@router.get("/documents/{doc_id}")
async def get_doc(doc_id: str):
    doc = await collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc["_id"] = str(doc["_id"])
    return doc