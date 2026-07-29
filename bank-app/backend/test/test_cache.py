import pytest
from unittest.mock import patch
from redis_cache import get_cached, set_cached, delete_cache
import json

"""

- normal workflow

get_cached()
        ↓
redis_client.get(...)
        ↓
Real Redis Server

- with @patch

get_cached()
        ↓
Fake redis_client.get(...)
        ↓
No Redis server

- “Temporarily replace redis_client.get inside the redis_cache module with a fake function while this test runs.”

get_cached()
      │
      ▼
Fake redis_client.get()
      │
      ▼
Whatever I tell it to return
"""


@patch("redis_cache.redis_client.get")
def test_get_cached_hit(mock_get):
    mock_get.return_value = json.dumps({"id": 1, "owner_name": "John"})

    result = get_cached("accounts:user:1")

    assert result == {"id": 1, "owner_name": "John"}


@patch("redis_cache.redis_client.get")
def test_get_cached_miss(mock_get):
    mock_get.return_value = None

    result = get_cached("accounts:user:1")

    assert result is None


@pytest.mark.asyncio
async def test_get_cached_from_redis_cache():
    key = "accounts:user:1"

    data = {"id": 1, "owner_name": "John"}

    set_cached(key, data)

    cached = get_cached(key)

    assert cached == data

    delete_cache(key)
