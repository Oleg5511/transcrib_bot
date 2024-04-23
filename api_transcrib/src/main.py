import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import transcrib_api
from core.config import get_settings
from core.logger import LOGGING
from db.create_data import create_user_balance

from db.postgres import purge_database, create_database

config = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация настроек до запуска сервиса"""


    await purge_database()
    await create_database()
    await create_user_balance()
    yield

app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description=config.project_description,
    version=config.project_version,
    lifespan=lifespan,
)

app.include_router(transcrib_api.router, prefix="/api/v1/transcrib", tags=["transcrib"])


if __name__ == "__main__":
    # asyncio.run(create_user_balance(async_session=async_session))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

