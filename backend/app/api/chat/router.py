from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.ai.ai_router import get_ai_response
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    try:
        messages = [
            {
                "role": "system",
                "content": "You are ARIA, a personal AI assistant. Be concise — max 2 lines unless detailed output is needed."
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
        response = get_ai_response(messages)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))