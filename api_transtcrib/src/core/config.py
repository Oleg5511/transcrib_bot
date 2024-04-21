import os
from logging import config as logging_config

from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = Field(
        "Система аутентификации и авторизации пользователей",
        description="Название проекта",
    )
    project_description: str = Field(
        "Система позволяет провести аутентификацию и авторизацию пользователей",
        description="Описание проекта",
    )
    project_version: str = Field("0.0.1", description="Версия проекта")

    # Настройки Redis
    redis_host: str = Field("127.0.0.1", description="Redis хост")
    redis_port: int = Field(6379, description="Redis порт")

    # Настройки Postgres
    postgres_db: str = Field("auth_database", description="Название БД Postgres")
    postgres_user: str = Field("auth", description="Пользователь Postgres")
    postgres_password: str = Field("123auth", description="Пароль Postgres")
    postgres_host: str = Field("127.0.0.1", description="Хост Postgres")
    postgres_port: int = Field(5432, description="Порт Postgres")

    # Корень проекта
    base_dir: str = Field(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        description="Базовая директория",
    )

    # Секретная фраза для токена
    token_phrase: str = Field(os.environ.get("TOKEN_PHRASE"), description="Ключ токена")

    is_debug_mode: bool = Field(False, description="Флаг работы в режиме отладки")

    admin_role_name: str = Field("admin", description="Название админской роли")

    req_per_min_by_token: int = Field(2, description='Количество запросов от авторизованного пользователя за минуту')
    req_per_min_common: int = Field(2, description='Общее количество запросов на ручку')
    req_per_min_by_email: int = Field(2, description='Количество запросов от неавторизованного пользователя за минуту')

conf: Settings | None = None


def get_settings() -> Settings:
    global conf

    if not conf:
        conf = Settings()
    return conf
