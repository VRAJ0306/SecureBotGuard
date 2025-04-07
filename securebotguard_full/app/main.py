from fastapi import FastAPI, Request
from pydantic import BaseModel
import time
from app.security import sanitize_input, check_prompt_injection
from app.chatbot_api import get_chatbot_response

app = FastAPI()

class ChatRequest(BaseModel):
    user_id: str
    message: str

user_requests = {}

@app.post("/secure-chat")
async def secure_chat(req: ChatRequest):
    user_id = req.user_id
    user_msg = sanitize_input(req.message)

    now = time.time()
    user_requests.setdefault(user_id, [])
    user_requests[user_id] = [t for t in user_requests[user_id] if now - t < 60]
    if len(user_requests[user_id]) >= 10:
        return {"error": "Rate limit exceeded"}

    user_requests[user_id].append(now)

    if check_prompt_injection(user_msg):
        return {"error": "Suspicious input detected. Request denied."}

    output = get_chatbot_response(user_msg)
    return {"response": output}
