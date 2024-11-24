import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings():
    database_url = os.getenv("DATABASE_URL")
    cloudinary_cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    cloudinary_api_key = os.getenv("CLOUDINARY_API_KEY")
    cloudinary_api_secret = os.getenv("CLOUDINARY_API_SECRET")
    debug_mode = os.getenv("DEBUG", "false").lower() == "true"

@lru_cache
def get_settings():
    return Settings()