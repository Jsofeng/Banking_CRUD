import os
import redis
import json
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

load_dotenv()

# without decode_responses = True -> b'{"id":1,"owner_name":"Jonathan"}'
# with decode_responses = True -> b'{"id":1,"owner_name":"Jonathan"}'

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(redis_url, decode_responses=True)


# cache hit or miss check
def get_cached(key):
    cached_data = redis_client.get(key)

    if cached_data:
        logger.info(f"CACHE HIT: {key}")
        return json.loads(cached_data)

    logger.info(f"CACHE MISS: {key}")
    return None


"""
set_cached(
    "accounts:user:42",
    accounts,
    ttl=60
)


accounts:user:42

[
 {
   "id":1,
   "owner_name":"Jonathan"
 }
]


expires in 60 secs then redis deletes it
"""


def set_cached(key, value, ttl=60):
    redis_client.set(key, json.dumps(value), ex=ttl)


def delete_cache(key):
    logger.info(f"CACHE INVALIDATED: {key}")
    redis_client.delete(key)
