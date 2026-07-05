from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.services.memory.memory_service import MemoryService
from app.services.embeddings.embeddings_service import EmbeddingsService
from app.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/memory", tags=["memory"])

class SearchRequest(BaseModel):
    query: str
    n_results: int = 3

@router.get("/history")
def get_history(limit: int = 20, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        memory_service = MemoryService(db, current_user.id)
        return memory_service.get_recent_history(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
def search_memory(request: SearchRequest, current_user=Depends(get_current_user)):
    try:
        embeddings_service = EmbeddingsService(current_user.id)
        results = embeddings_service.search(request.query, n_results=request.n_results)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))