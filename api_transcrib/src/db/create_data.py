from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import async_session
from models import UserBalance


async def create_user_balance() -> str:
    async with async_session() as session:
        ub = UserBalance(user_id='23bbdc04-66dc-41ea-a315-7ec302df478d', balance=100)
        session.add(ub)
        await session.commit()
    return f'Создан пользователь с ID 23bbdc04-66dc-41ea-a315-7ec302df478d'
