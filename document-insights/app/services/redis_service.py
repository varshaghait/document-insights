from app.database import redis

async def increment_user_jobs(user_id):
    key = f"user:{user_id}:jobs"
    return await redis.incr(key)

async def decrement_user_jobs(user_id):
    key = f"user:{user_id}:jobs"
    return await redis.decr(key)

async def get_user_jobs(user_id):
    key = f"user:{user_id}:jobs"
    val = await redis.get(key)
    return int(val) if val else 0

async def cache_summary(content_hash, summary):
    await redis.set(f"hash:{content_hash}", summary, ex=3600)

async def get_cached_summary(content_hash):
    return await redis.get(f"hash:{content_hash}")