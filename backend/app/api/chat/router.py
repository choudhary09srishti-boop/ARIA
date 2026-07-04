from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai.ai_router import get_ai_response
from app.services.memory.memory_service import MemoryService
from app.services.personality.personality_service import PersonalityService
from app.middleware.auth_middleware import get_current_user
from app.database.db import get_db

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        memory_service = MemoryService(db, current_user.id)
        personality_service = PersonalityService(db, current_user.id)

        history = memory_service.get_recent_history(limit=10)
        system_prompt = personality_service.get_system_prompt()

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": request.message})

        response = get_ai_response(messages)
        memory_service.save_interaction(request.message, response)

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))