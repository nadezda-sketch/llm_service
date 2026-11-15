import logging
import json
from fastapi import FastAPI
from pydantic import BaseModel, Field
from services.logic import process_request

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        if hasattr(record, 'key'):
            log_record['cache_key'] = record.key
        return json.dumps(log_record)

logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = FastAPI(title="LLM Service")

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    logger.info(f"Received request: {request.message[:50]}...")
    result = process_request(request.message)
    return result
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
