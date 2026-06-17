from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TranslateRequest(BaseModel):
    text: str
    direction: str = "en-ru" # en-ru или ru-en

class TranslateResponse(BaseModel):
    result: str
    model_name: str
    direction: str

class HistoryItem(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    direction: str
    created_at: datetime

    class Config:
        from_attributes = True