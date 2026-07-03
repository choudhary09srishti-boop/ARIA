from sqlalchemy.orm import Session
from datetime import datetime
import uuid

class MemoryService:
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id

    def save_interaction(self, user_message: str, aria_response: str):
        from app.models.memory import Memory
        memory = Memory(
            id=str(uuid.uuid4()),
            user_id=self.user_id,
            user_message=user_message,
            aria_response=aria_response,
            created_at=datetime.utcnow()
        )
        self.db.add(memory)
        self.db.commit()

    def get_recent_history(self, limit: int = 10) -> list:
        from app.models.memory import Memory
        records = (
            self.db.query(Memory)
            .filter(Memory.user_id == self.user_id)
            .order_by(Memory.created_at.desc())
            .limit(limit)
            .all()
        )
        history = []
        for r in reversed(records):
            history.append({"role": "user", "content": r.user_message})
            history.append({"role": "assistant", "content": r.aria_response})
        return history