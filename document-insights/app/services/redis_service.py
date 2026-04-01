from app.database import redis

async def increment_user_jobs(user_id):
    key = f"user:{user_id}:jobs"
    val = await redis.incr(key)
    await redis.expire(key, 3600)
    return val

async def decrement_user_jobs(user_id):
    key = f"user:{user_id}:jobs"
    val = await redis.decr(key)
    if val < 0:
        await redis.set(key, 0)
    return val

async def get_user_jobs(user_id):
    key = f"user:{user_id}:jobs"
    val = await redis.get(key)
    return int(val) if val else 0

async def cache_summary(content_hash, summary):
    await redis.set(f"hash:{content_hash}", summary, ex=3600)

async def get_cached_summary(content_hash):
    return await redis.get(f"hash:{content_hash}")