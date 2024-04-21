import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

# from api.v1 import user_api, profile_api, history_api, roles_api
from core.config import get_settings
from core.logger import LOGGING

from db import redis
from db.postgres import purge_database, create_database

config = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация настроек до запуска сервиса"""

    # В режиме отладки создаем таблицы БД через sqlalchemy
    if config.is_debug_mode is True:
        # Импорт моделей необходим для их автоматического создания
        from models.models import User, HistoryEvent, TokenBase

        await create_database()

    redis.redis = Redis(
        host=config.redis_host, port=config.redis_port, db=0, decode_responses=True
    )
    yield
    await redis.redis.close()
    await purge_database()


app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description=config.project_description,
    version=config.project_version,
    lifespan=lifespan,
)

# app.include_router(roles_api.router, prefix="/api/v1/roles", tags=["roles"])
# app.include_router(user_api.router, prefix="/api/v1/user_api", tags=["user_api"])
# app.include_router(profile_api.router, prefix="/api/v1/profile", tags=["profile"])
# app.include_router(history_api.router, prefix="/api/v1/history", tags=["history"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
