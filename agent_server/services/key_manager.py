import os
import threading
from itertools import cycle
from dotenv import load_dotenv


load_dotenv()


class APIKeyManager:
    def __init__(self):
        keys = os.getenv("GOOGLE_API_KEYS")

        if not keys:
            # Fallback to single key if GOOGLE_API_KEYS is not set
            single_key = os.getenv("GOOGLE_API_KEY")
            if not single_key:
                raise ValueError("Neither GOOGLE_API_KEYS nor GOOGLE_API_KEY is set")
            self.keys = [single_key]
        else:
            self.keys = [k.strip() for k in keys.split(",")]
        
        self.index = 0
        self.lock = threading.Lock()

    def get_key(self):
        with self.lock:
            key = self.keys[self.index]
            return key

    def switch_key(self):
        with self.lock:
            self.index = (self.index + 1) % len(self.keys)
            return self.keys[self.index]


# global singleton (important)
key_manager = APIKeyManager()
