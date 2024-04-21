from uuid import uuid4, UUID
from pydantic import Field, EmailStr
from schemas.base_schema import OrjsonBaseModel
from datetime import datetime, timezone

class FileInfo(OrjsonBaseModel):
    """Модель профиля"""

    file_id: UUID = Field(examples=[uuid4()], description="Идентификатор файла")
    user_id: UUID = Field(examples=[uuid4()], description="Идентификатор пользователя")
    file_name: str = Field(examples=[uuid4()], description="Название файла")
    file_lenth: int = Field(examples=[uuid4()], description="Название файла")
    create_dttm: datetime = Field(default_factory=lambda: datetime.now(timezone.utc),
                                  description="Момент создания записи")

class FileInDB(OrjsonBaseModel):
    file_id: UUID
    user_id: str
    file_lenth: str
    total_time: str

class ToTranscrib(OrjsonBaseModel):
    file_id: UUID
    user_id: UUID

class FromTranscrib(OrjsonBaseModel):
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