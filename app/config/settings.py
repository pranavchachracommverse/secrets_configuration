import os
from dotenv import load_dotenv

load_dotenv(override=True)

APP_ENV = os.environ.get("APP_ENV", "dev")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
REGION_NAME = os.environ.get("REGION_NAME", "us-east-1")
APP_BASE_PATH = os.environ.get("APP_BASE_PATH", "Platform/Admin")
