import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:5001/api")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")