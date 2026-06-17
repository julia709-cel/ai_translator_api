import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.db import init_db
from app.routes import analyze, history

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск сервиса AI Translator API...")
    await init_db()
    yield
    logger.info("Остановка сервиса.")

app = FastAPI(title="AI Translator API", lifespan=lifespan)

# Подключаем роуты
app.include_router(analyze.router, tags=["Analysis"])
app.include_router(history.router, tags=["History"])

# Подключаем статические файлы (UI)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root_ui():
    return FileResponse("app/static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}