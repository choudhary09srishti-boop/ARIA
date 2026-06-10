from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from groq import Groq
from app.config.settings import settings
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/chat", tags=["chat"])

client = Groq(api_key=settings.GROQ_API_KEY)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are ARIA, a personal AI assistant. Be concise — max 2 lines unless detailed output is needed."
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ],
            max_tokens=200
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))