import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv

# get_remote_address uses the user’s IP address as the identifier.
"""
User A -> 192.168.1.10 -> 5 requests/min
User B -> 192.168.1.20 -> 5 requests/min
"""

load_dotenv()

limiter = Limiter(
    key_func=get_remote_address,  # “Use the user’s IP address to track limits.”
    storage_uri=os.getenv(  # “Where should I store request counts?”
        "REDIS_URL", "redis://localhost:6379"
    ),
)
