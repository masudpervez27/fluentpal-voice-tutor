import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from .core.config import settings


def configure_logging() -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", settings.log_level).upper()
    level = getattr(logging, level_name, logging.INFO)
    root_logger = logging.getLogger()

    if not root_logger.handlers:
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        )
    else:
        root_logger.setLevel(level)

    return logging.getLogger("fluentpal-voice-tutor.main")


logger = configure_logging()

app = FastAPI(
    title=settings.app_name,
    description="Realtime voice tutoring starter with transcript and correction pipeline placeholders.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.on_event("startup")
async def startup() -> None:
    logger.info("FluentPal Voice Tutor backend startup complete")
