import os
import logging
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        self.pipelines = {}
        self.models = {
            "en-ru": os.getenv("HF_MODEL_EN_RU", "Helsinki-NLP/opus-mt-en-ru"),
            "ru-en": os.getenv("HF_MODEL_RU_EN", "Helsinki-NLP/opus-mt-ru-en")
        }

    def get_pipeline(self, direction: str):
        if direction not in self.models:
            raise ValueError(f"Неподдерживаемое направление: {direction}")
            
        if direction not in self.pipelines:
            model_name = self.models[direction]
            logger.info(f"Загрузка модели {model_name} (это может занять время при первом запуске)...")
            try:
                # Используем device=-1 для CPU
                self.pipelines[direction] = pipeline("translation", model=model_name, device=-1)
                logger.info(f"Модель {model_name} успешно загружена.")
            except Exception as e:
                logger.error(f"Ошибка загрузки модели HF: {e}")
                raise RuntimeError("Ошибка загрузки модели Hugging Face")
        return self.pipelines[direction]

    def translate(self, text: str, direction: str):
        pipe = self.get_pipeline(direction)
        result = pipe(text, max_length=400)
        return result[0]['translation_text']

ml_service = MLService()