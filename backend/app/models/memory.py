from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.database.db import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    user_message = Column(Text, nullable=False)
    aria_response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())