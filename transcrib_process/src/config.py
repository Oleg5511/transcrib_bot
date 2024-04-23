import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from logger import LOGGING


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

class Settings(BaseSettings):
    project_version: str = Field("0.0.1", description="Версия проекта")

    # Корень проекта
    base_dir: str = Field(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description="Базовая директория",
    )
    # Настройки Postgres
    postgres_db: str = Field("transcrib", description="Название БД Postgres")
    postgres_user: str = Field("postgres", description="Пользователь Postgres")
    postgres_password: str = Field("postgres", description="Пароль Postgres")
    postgres_host: str = Field("127.0.0.1", description="Хост Postgres")
    postgres_port: int = Field(5432, description="Порт Postgres")


    # Настройки Kafka
    kafka_host: list = Field(["localhost"], description="Kafka хост")
    kafka_port: int = Field(9094, description="Kafka порт")
    num_partitions: int = Field(3, description="Количество партиций Кафки")
    replication_factor: int = Field(2, description="Количество реплик Кафки")
    topic_name: list = Field(["for_transcrib", "from_transcrib"], description="Топики кафка")

conf: Settings | None = None


def get_settings() -> Settings:
    global conf

    if not conf:
        conf = Settings()
    return conf
