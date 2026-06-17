import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import AsyncSessionLocal
from app.models import RequestHistory
from app.schemas import TranslateRequest, TranslateResponse
from app.ml_service import ml_service

router = APIRouter()
logger = logging.getLogger(__name__)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/analyze", response_model=TranslateResponse)
async def analyze_text(req: TranslateRequest, db: AsyncSession = Depends(get_db)):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Текст запроса не может быть пустым")

    try:
        # Перевод
        translated_text = ml_service.translate(req.text, req.direction)
        model_name = ml_service.models[req.direction]
        
        # Сохранение в БД
        db_record = RequestHistory(
            input_text=req.text,
            result_text=translated_text,
            model_name=model_name,
            direction=req.direction
        )
        db.add(db_record)
        await db.commit()
        await db.refresh(db_record)
        
        logger.info(f"Успешный запрос: {req.direction} | ID: {db_record.id}")
        return TranslateResponse(result=translated_text, model_name=model_name, direction=req.direction)
        
    except RuntimeError as e:
        logger.error(f"Ошибка модели: {e}")
        raise HTTPException(status_code=500, detail="Ошибка работы модели Hugging Face")
    except Exception as e:
        logger.error(f"Ошибка БД или сервера: {e}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")