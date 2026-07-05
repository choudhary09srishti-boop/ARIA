from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.services.ai.ai_router import get_ai_response
from app.services.memory.memory_service import MemoryService
from app.services.personality.personality_service import PersonalityService
from app.services.embeddings.embeddings_service import EmbeddingsService
from app.middleware.auth_middleware import get_current_user
from app.database.db import get_db
import uuid

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
        embeddings_service = EmbeddingsService(current_user.id)

        history = memory_service.get_recent_history(limit=10)
        relevant_context = embeddings_service.search(request.message, n_results=3)
        system_prompt = personality_service.get_system_prompt()

        if relevant_context:
            context_text = "\n".join(relevant_context)
            system_prompt += f"\n\nRelevant past context:\n{context_text}"

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": request.message})

        response = get_ai_response(messages)

        memory_service.save_interaction(request.message, response)
        embeddings_service.store(
            text=f"User: {request.message}\nARIA: {response}",
            doc_id=str(uuid.uuid4()),
            metadata={"user_id": current_user.id}
        )

        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))