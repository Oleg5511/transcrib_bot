from fastapi import APIRouter, Depends, HTTPException, Body
from http import HTTPStatus

from typing import Annotated
from uuid import UUID

from redis.asyncio.client import Redis

from db.redis import get_redis
from helpers.helpers import check_role
from schemas.roles_schemas import RoleInDB
from services.roles_service import get_roles_service, RolesService
router = APIRouter()

from core.config import get_settings
settings = get_settings()


@router.get(
    path="/",
    summary="Список Ролей",
    description="Возвращает список ролей присутствующих в сервисе авторизации",
    response_model=list[RoleInDB],
    response_description="Список Моделей",
)
async def roles_list(
        roles_service: RolesService = Depends(get_roles_service)
) -> RoleInDB:
    return await roles_service.roles_list()


@router.post(
    path="/grant",
    summary="Добавить роль",
    description="Добавляет роль указанному пользователю",
)
@check_role(permission_role=settings.admin_role_name)
async def grant_role(
        access_token: Annotated[
            str, Body(description="Токен доступа", title="Токен доступа")
        ],
        user_id: Annotated[
            UUID, Body(description="ID пользователя", title="ID пользователя")
        ],
        role: Annotated[
            str, Body(description="Роль пользователя", title="Роль пользователя")
        ],
        role_service: RolesService = Depends(get_roles_service),
        redis: Redis = Depends(get_redis),
):
    try:
        await role_service.grant_role(user_id, role)
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(exc))


@router.post(
    path="/revoke",
    summary="Отобрать роль",
    description="Отнимает роль у указанного пользователя",
)
@check_role(permission_role='admin')
async def revoke_role(
    access_token: Annotated[
        str, Body(description="Токен доступа", title="Токен доступа")
    ],
    user_id: Annotated[
        UUID, Body(description="ID пользователя", title="ID пользователя")
    ],
    role: Annotated[
        str, Body(description="Роль пользователя", title="Роль пользователя")
    ],
    role_service: RolesService = Depends(get_roles_service),
    redis: Redis = Depends(get_redis),
):
    try:
        await role_service.revoke_role(user_id, role)
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(exc))


@router.post(
    path='/add',
    summary='Добавить роль',
    description='Добавляет роль в бд'
)
@check_role(permission_role='admin')
async def add_role(
        name: Annotated[str, Body(description="Создаваемая роль")],
        access_token: Annotated[str, Body(description="Токен доступа", title="Токен доступа")],
        role_service: RolesService = Depends(get_roles_service),
        redis: Redis = Depends(get_redis),
):
    try:
        await role_service.add_role(name)
    except Exception as exc:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(exc))

