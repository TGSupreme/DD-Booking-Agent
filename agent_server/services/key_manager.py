import os
import threading
from itertools import cycle
from dotenv import load_dotenv


load_dotenv()


class APIKeyManager:
    def __init__(self):
        keys = os.getenv("GOOGLE_API_KEYS")

        if not keys:
            raise ValueError("GOOGLE_API_KEYS not set")

        self.keys = [k.strip() for k in keys.split(",")]
        self.pool = cycle(self.keys)
        self.lock = threading.Lock()   # thread-safe

    def get_key(self):
        with self.lock:
            return next(self.pool)


# global singleton (important)
key_manager = APIKeyManager()
