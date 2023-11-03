import os
import redis

redis_client = redis.Redis.from_url(os.environ['REDIS_URI'], decode_responses=True)
