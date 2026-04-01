# after redis init
redis = Redis.from_url(REDIS_URL, decode_responses=True)

# add ping check
async def check_connections():
    await redis.ping()
    await db.command("ping")