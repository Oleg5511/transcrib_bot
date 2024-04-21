from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException, Depends, Body
from redis.asyncio.client import Redis

from db.redis import get_redis
from helpers.helpers import is_access_token_valid
from schemas.schemas_entity import AccessToken
from schemas.schemas_history import PaginatedHistoryEventSchema
from services.history_serv import (
    HistoryService,
    get_history_service,
)

router = APIRouter()


@router.post(
    "/auth_events",
    response_model=PaginatedHistoryEventSchema,
    summary="Получить историю входов и выходов пользователя",
    description="Получить историю входов и выходов пользователя",
)
async def get_history_auth_events(
    access_token: Annotated[
        str, Body(description="Токен доступа", title="Токен доступа")
    ],
    page_number: Annotated[
        int, Body(description="Номер страницы", ge=1, le=10000, title="Номер страницы")
    ] = 1,
    page_size: Annotated[
        int,
        Body(
            description="Количество элементов на странице",
            ge=1,
            le=10000,
            title="Количество элементов на странице",
        ),
    ] = 10,
    redis: Redis = Depends(get_redis),
    history_service: HistoryService = Depends(get_history_service),
) -> PaginatedHistoryEventSchema:
    """Ручка для получения истории входов и выходов пользователя"""

    # Проверяем токен
    if not await is_access_token_valid(access_token=access_token, redis=redis):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Token not valid")

    # Получаем user_id
    decoded_payload = jwt.decode(
        access_token, "some_secret_phrase", algorithms=["HS256"]
    )
    user_id = decoded_payload["user_id"]

    # Получаем историю
    paginated_history_events_schema = await history_service.get_history_events(
        user_id=user_id, page_number=page_number, page_size=page_size
    )
    if not paginated_history_events_schema:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    return paginated_history_events_schema
