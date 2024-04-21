import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from db.postgres import Base

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    create_dttm = Column(DateTime, default=datetime.utcnow)
    name = Column(String(255), nullable=True)
    telegram_nick = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False)

    def __init__(
        self, create_dttm: str, name: str, telegram_nick: datetime, email: str
    ) -> None:
        self.create_dttm = create_dttm
        self.name = name
        self.telegram_nick = telegram_nick
        self.email = email


    def __repr__(self) -> str:
        return f"<User {self.id}, {self.create_dttm}, {self.name}, {self.telegram_nick}, " \
               f"{self.email}>"


class File(Base):
    __tablename__ = "files"

    file = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        unique=False,
        nullable=False
    )
    file_name = Column(String(255))
    file_lenth = Column(String(255))
    create_dttm = Column(DateTime, default=datetime.utcnow)


    def __init__(
        self, user_id: str, file_name: str, file_lenth: str, create_dttm: datetime
    ) -> None:
        self.user_id = user_id
        self.file_name = file_name
        self.file_lenth = file_lenth
        self.create_dttm = create_dttm


    def __repr__(self) -> str:
        return f"<File {self.file_id}, {self.user_id}, {self.file_name}, {self.file_lenth}, " \
               f"{self.create_dttm}>"

class AnalysisProcess(Base):
    __tablename__ = "analysis_process"

    proc_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    file_id = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False
    )
    create_dttm = Column(DateTime, default=datetime.utcnow)
    file_lenth = Column(Integer)


    def __init__(
        self, proc_id: str, file_id: str, create_dttm: str, file_lenth: str
    ) -> None:
        self.proc_id = proc_id
        self.file_id = file_id
        self.create_dttm = create_dttm
        self.file_lenth = file_lenth


    def __repr__(self) -> str:
        return f"<AnalysisProcess {self.proc_id}, {self.file_id}, {self.create_dttm}, {self.file_lenth}>"

class UserBalance(Base):
    __tablename__ = "user_balance"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    balance = Column(Integer)

    def __init__(
        self, balance: str
    ) -> None:
        self.balance = balance


    def __repr__(self) -> str:
        return f"<UserBalance {self.user_id}, {self.balance}>"