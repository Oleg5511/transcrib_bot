import abc

from sqlalchemy.ext.asyncio import AsyncSession


class BaseService(abc.ABC):
    """Базовый сервис"""

    def __init__(self, session: AsyncSession):
        self.session = session
