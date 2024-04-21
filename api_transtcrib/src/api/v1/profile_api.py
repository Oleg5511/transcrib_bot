from http import HTTPStatus
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException, Depends, Body, Header
from redis.asyncio.client import Redis


from db.redis import get_redis
from helpers.helpers import is_access_token_valid
from schemas.schemas_entity import AccessToken
from services.profile_serv import get_profile_service, ProfileService, ProfileSchema

router = APIRouter()


@router.post(
    "/",
    response_model=ProfileSchema,
    summary="Получить профиль пользователя",
    description="Получить профиль пользователя",
)
async def get_profile(
    access_token: Annotated[
        AccessToken, Body(description="Токен доступа", title="Токен доступа")
    ],
    redis: Redis = Depends(get_redis),
    profile_service: ProfileService = Depends(get_profile_service),
) -> ProfileSchema:
    """Ручка для отображения профиля пользователя"""

    # Проверяем токен
    if not await is_access_token_valid(
        access_token=access_token.access_token, redis=redis
    ):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Token not valid")

    # Получаем user_id
    decoded_payload = jwt.decode(
        access_token.access_token, "some_secret_phrase", algorithms=["HS256"]
    )
    user_id = decoded_payload["user_id"]

    # Пролучаем профиль
    profile = await profile_service.get_profile(user_id=user_id)
    if not profile:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User profile not found"
        )
    return profile


@router.patch(
    "/",
    response_model=ProfileSchema,
    summary="Изменить профиль пользователя",
    description="Изменить профиль пользователя",
)
async def change_profile(
    access_token: Annotated[
        str, Body(description="Токен доступа", title="Токен доступа")
    ],
    email: Annotated[str | None, Body(description="Почта", title="Почта")] = None,
    password: Annotated[str | None, Body(description="Пароль", title="Пароль")] = None,
    first_name: Annotated[
        str | None, Body(description="Имя пользователя", title="Имя пользователя")
    ] = None,
    last_name: Annotated[
        str | None,
        Body(description="Фамилия пользователя", title="Фамилия пользователя"),
    ] = None,
    redis: Redis = Depends(get_redis),
    profile_service: ProfileService = Depends(get_profile_service),
):
    """Ручка для изменения профиля пользователя"""

    # Проверяем токен
    if not await is_access_token_valid(access_token=access_token, redis=redis):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail="Token not valid")

    # Получаем user_id
    decoded_payload = jwt.decode(
        access_token, "some_secret_phrase", algorithms=["HS256"]
    )
    user_id = decoded_payload["user_id"]

    profile = await profile_service.change_profile(
        user_id=user_id,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    if not profile:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User profile not found"
        )

    return profile
