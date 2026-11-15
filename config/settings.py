import os
from dotenv import load_dotenv

load_dotenv()

YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")
MODEL_NAME = "yandexgpt-lite"
TEMPERATURE = 0.3
MAX_TOKENS = 1000

TIMEOUT_SECONDS = 10
MAX_RETRIES = 3
RETRY_DELAY = 2

CACHE_TTL_SECONDS = 600
