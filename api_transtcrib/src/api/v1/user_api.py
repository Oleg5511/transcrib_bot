from http import HTTPStatus
from typing import Annotated

from redis.asyncio import Redis
from fastapi import Depends, APIRouter, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres import get_session
from schemas.schemas_entity import UserInDB, UserCreate, UserLogIn, Tokens, RefreshToken
from core.config import get_settings
from db.redis import get_redis
from services.user_serv import UserService, get_user_service
from services.history_serv import HistoryService, get_history_service
from helpers.helpers import request_count_by_token, request_count_by_mail

router = APIRouter()
config = get_settings()


@router.post("/signup", response_model=UserInDB, status_code=HTTPStatus.CREATED)
@request_count_by_mail()
async def create_user_api(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
) -> UserInDB:
    """Функция регистрирует пользователя, записывая его данные в БД"""

    return await user_service.create_user(user_create=user_create, db=db)


@router.post("/login", response_model=Tokens, status_code=HTTPStatus.OK)
@request_count_by_mail()
async def login_user_api(
    login_params: UserLogIn,
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    history_service: HistoryService = Depends(get_history_service),
    user_agent: Annotated[str | None, Header()] = None,
) -> Tokens:
    """Функция логинит пользователя и выдает ему access_token и refresh_token"""

    return await user_service.login_user(
        login_params=login_params,
        db=db,
        history_service=history_service,
        user_agent=user_agent,
    )

# ToDO Подумать, надо ли делать ограничение запросов через какой то абстрактный класс, чтобы к каждой ручке декоратор не прикручивать
@router.post("/logout", response_model=str, status_code=HTTPStatus.OK)
@request_count_by_token()
async def logout_user_api(
    tokens: Tokens,
    redis: Redis = Depends(get_redis),
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
    history_service: HistoryService = Depends(get_history_service),
    user_agent: Annotated[str | None, Header()] = None,
) -> str:
    """Функция разлогинивает пользователя. access_token добавляется в редис, а refresh_token удаляется из БД"""

    try:
        return await user_service.logout_user_api(
            tokens=tokens,
            redis=redis,
            db=db,
            history_service=history_service,
            user_agent=user_agent,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/refresh_auth", response_model=Tokens, status_code=HTTPStatus.OK)
@request_count_by_token()
async def refresh_auth_api(
    refresh_token: RefreshToken,
    db: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
) -> Tokens:
    """Функция для получения нового access_token по refresh_token"""
    return await user_service.refresh_auth(refresh_token=refresh_token, db=db)
