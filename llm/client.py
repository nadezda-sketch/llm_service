import requests
import time
import logging
from config.settings import (
    YANDEX_API_KEY, YANDEX_FOLDER_ID, MODEL_NAME, 
    TEMPERATURE, MAX_TOKENS, TIMEOUT_SECONDS, MAX_RETRIES, RETRY_DELAY
)

logger = logging.getLogger(__name__)

def call_llm(prompt: str) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "modelUri": f"gpt://{YANDEX_FOLDER_ID}/{MODEL_NAME}",
        "completionOptions": {
            "stream": False,
            "temperature": TEMPERATURE,
            "maxTokens": MAX_TOKENS
        },
        "messages": [
            {"role": "system", "text": "Ты — полезный ассистент. Отвечай кратко и по делу."},
            {"role": "user", "text": prompt}
        ]
    }

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"LLM call attempt {attempt + 1}")
            response = requests.post(url, headers=headers, json=data, timeout=TIMEOUT_SECONDS)
            
            if response.status_code >= 500:
                raise requests.exceptions.HTTPError(f"Server error: {response.status_code}")
            
            response.raise_for_status()
            result = response.json()
            return result['result']['alternatives'][0]['message']['text']
            
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                logger.error("All retries failed.")
                raise Exception("LLM Service Unavailable")
            time.sleep(RETRY_DELAY * (2 ** attempt))
