import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """Декодируем, тк orjson.dumps возвращает bytes, а pydantic требует unicode"""
    return orjson.dumps(v, default=default).decode()


class OrjsonBaseModel(BaseModel):
    """Базовая модель с оптимизацией сериализации"""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
