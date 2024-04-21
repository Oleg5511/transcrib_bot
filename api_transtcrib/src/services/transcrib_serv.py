from http import HTTPStatus
from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from functools import lru_cache
from schemas.schemas import FileInfo, FileInDB
# from schemas.schemas_entity import UserInDB
from core.config import get_settings
from db.postgres import get_session
from models.models import File
from services.base_serv import BaseService

config = get_settings()


class TranscribService(BaseService):
    """Сервис транскрибации"""

    async def start_transcrib(self, file_info: FileInfo, db: AsyncSession) -> FileInDB:
        """Функция записывает в БД информацию о файле и отправляет сообщение в кафку"""

        transcrib_dto = jsonable_encoder(file_info)
        file = File(**transcrib_dto)
        try:
            db.add(file)
            await db.commit()
            await db.refresh(file)
            return file
        except IntegrityError as ex:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="File already exists"
            )
        send_to_transcrib(message)


@lru_cache
def get_transcrib_service(
    session: AsyncSession = Depends(get_session),
) -> TranscribService:
    """Возвращает синглтон сервиса"""
    return TranscribService(session=session)
