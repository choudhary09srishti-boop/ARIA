from fastapi import APIRouter, Depends
from middleware.auth_middleware import get_current_user
from services.ai.ai_router import get_ai_response
from services.memory.memory_service import save_conversation
from services.embeddings.embeddings_service import store_embedding
import re

router = APIRouter()

def clean_for_speech(text: str) -> str:
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\n+', ' ', text)
    return text.strip()

@router.post("/speak")
async def voice_chat(payload: dict, user=Depends(get_current_user)):
    user_text = payload.get("text", "")
    ai_reply = await get_ai_response(user_text, user_id=user.id)
    clean_reply = clean_for_speech(ai_reply)
    save_conversation(user.id, user_text, ai_reply)
    store_embedding(user.id, user_text, ai_reply)
    return {"reply": clean_reply}