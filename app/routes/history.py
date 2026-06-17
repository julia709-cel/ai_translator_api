import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import AsyncSessionLocal
from app.models import RequestHistory
from app.schemas import HistoryItem

router = APIRouter()
logger = logging.getLogger(__name__)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.get("/history", response_model=list[HistoryItem])
async def get_history(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RequestHistory).order_by(RequestHistory.created_at.desc()).limit(20))
        return result.scalars().all()
    except Exception as e:
        logger.error(f"Ошибка получения истории: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

@router.get("/history/{item_id}", response_model=HistoryItem)
async def get_history_item(item_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(RequestHistory).where(RequestHistory.id == item_id))
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail="Запрос не найден")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения записи {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")