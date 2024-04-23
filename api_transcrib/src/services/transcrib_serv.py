import asyncio
import datetime
import time
from uuid import UUID, uuid4

from fastapi import HTTPException
from sqlalchemy import select, update, delete, insert
from schemas.schemas import FileInfo, Response, ForTranscrib
from core.config import get_settings
from db.postgres import async_session
from models import UserBalance, AnalysisProcess

config = get_settings()

async def init_transcrib(
    message: ForTranscrib
):
    """Запускает транскрибацию файла, сообщение с которым лежит в Кафке"""
    # Получили доступный баланс пользователя
    user_id = message.user_id
    file_id = message.file_id
    file_lenth = message.file_lenth
    async with async_session() as db:
        balance_data = await db.execute(select(UserBalance).where(UserBalance.user_id == user_id))
        in_process = await db.execute(select(AnalysisProcess).where(AnalysisProcess.user_id == user_id))

        user_balance = balance_data.scalars().first()
        if not user_balance:
            raise HTTPException(404, detail="User not in DB")
        curr_balance = user_balance.balance
        reserved_balance = in_process.scalars().first()

        new_balance = (curr_balance - reserved_balance.file_lenth
                       if reserved_balance else curr_balance)

        if new_balance < file_lenth:
            raise HTTPException(404, detail=f"Not enough balance, current balanc {new_balance}")

        # Сделать запись о начале обработки в Postgres
        await db.execute(insert(AnalysisProcess).values(user_id=user_id, file_id=file_id, file_lenth=file_lenth,
                                                        create_dttm=datetime.datetime.now(), proc_id=uuid4()))
        await db.commit()

        # Транскрибировать/анализировать файл
        asyncio.sleep(10)
        # analysed = analyse_file()

        # Изменить состояние баланса пользователя
        new_balance -= file_lenth
        await db.execute(
                update(UserBalance)
                .where(UserBalance.user_id == user_id)
                .values(balance=new_balance)
                )
        # Удалить запись из analysys_process
        await db.execute(
             delete(AnalysisProcess)
             .where((AnalysisProcess.user_id == user_id) & (AnalysisProcess.file_id == file_id))
         )
     # Комит обоих операций
        await db.commit()

    return Response(status_code='SUCCESS') # В ответе возвращать analysed из функции транскрибации
