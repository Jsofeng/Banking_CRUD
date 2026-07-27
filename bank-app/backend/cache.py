import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()

# without decode_responses = True -> b'{"id":1,"owner_name":"Jonathan"}'
# with decode_responses = True -> b'{"id":1,"owner_name":"Jonathan"}'

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.from_url(redis_url, decode_responses=True)


# cache hit or miss check
def get_cached(key):
    cached_data = redis_client.get(key)

    if cached_data:
        return json.loads(cached_data)

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
    redis_client.delete(key)
