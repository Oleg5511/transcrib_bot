from http import HTTPStatus
from uuid import uuid4, UUID
from pydantic import Field, EmailStr
from schemas.base_schema import OrjsonBaseModel
from datetime import datetime, timezone

class FileInfo(OrjsonBaseModel):
    """Модель профиля"""

    file_id: UUID = Field(examples=[uuid4()], description="Идентификатор файла")
    user_id: UUID = Field(examples=[uuid4()], description="Идентификатор пользователя")
    file_name: str = Field(examples=['file_name'], description="Название файла")
    file_lenth: int = Field(examples=[60], description="Название файла")
    create_dttm: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                  description="Момент создания записи")

class Response(OrjsonBaseModel):
    status_code: str

class ForTranscrib(OrjsonBaseModel):
    file_id: UUID
    user_id: UUID
    file_lenth: int

class FromTranscrib(OrjsonBaseModel):
    user_id: UUID
    file_id: UUID
    status_code: int
    result: str

    # class Config:
    #     from_attributes = True

# class GetUser(OrjsonBaseModel):
#     email: EmailStr | None = Field(default=None)
#     password: str
#     first_name: str = Field(default=None)
#     last_name: str = Field(default=None)