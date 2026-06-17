from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.sql import func
from app.db import Base

class RequestHistory(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    result_text = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    direction = Column(String, nullable=False) # Добавлено для переводчика
    created_at = Column(DateTime(timezone=True), server_default=func.now())