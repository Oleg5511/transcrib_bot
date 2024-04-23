import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from api.v1 import transcrib_api
from core.config import get_settings
from core.logger import LOGGING


from db.postgres import purge_database
from kafka_config.create_topic import create_topic
from kafka_config.kafka_config import get_kafka_consumer

config = get_settings()
consumer = get_kafka_consumer(topic=config.topic_name[0], group_id=config.topic_name[0])

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Инициализация настроек до запуска сервиса"""

    yield
    await purge_database()

create_topic(config)
app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    description=config.project_description,
    version=config.project_version,
    # lifespan=lifespan,
)

app.include_router(transcrib_api.router, prefix="/api/v1/transcrib", tags=["transcrib"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )

