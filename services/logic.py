import logging
from cache.cache_manager import cache
from llm.client import call_llm

logger = logging.getLogger(__name__)

def process_request(user_message: str) -> dict:
    cache_key = f"{user_message}"
    
    cached_response = cache.get(cache_key)
    if cached_response:
        logger.info("CACHE_HIT", extra={"key": cache_key})
        return {"response": cached_response, "source": "cache"}
    
    logger.info("CACHE_MISS", extra={"key": cache_key})

    try:
        llm_response = call_llm(user_message)
        cleaned_response = llm_response.strip()
        if not cleaned_response:
            raise ValueError("Empty response from LLM")
            
        cache.set(cache_key, cleaned_response)
        return {"response": cleaned_response, "source": "llm"}
        
    except Exception as e:
        logger.error(f"Service error: {e}")
        return {
            "response": "Сервис временно недоступен, попробуйте позже.", 
            "source": "fallback"
        }
