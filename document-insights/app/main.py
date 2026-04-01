from fastapi import FastAPI
from app.routes import documents, users
from app.database import create_indexes
import asyncio
from app.services.worker import worker

app = FastAPI()

app.include_router(documents.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup():
    await create_indexes()
    asyncio.create_task(worker())

@app.get("/health")
async def health():
    return {"status": "ok"}