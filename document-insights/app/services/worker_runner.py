import asyncio
from app.services.worker import worker

asyncio.run(worker())