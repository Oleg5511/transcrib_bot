import asyncio
import json
from sqlalchemy import select, update, delete, insert
from schemas.schemas import FileInfo, Response, ForTranscrib
from core.config import get_settings
from db.postgres import async_session

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
        balance_data = await db.execute(select(UserBalance).where(UserBalance.user_id == UUID(user_id))) #get_balance(user_id)
        in_process = await db.execute(select(AnalysisProcess).where(AnalysisProcess.user_id == UUID(user_id)))

        new_balance = balance_data.scalars().first().balance - in_process.scalars().first().file_lenth


        if new_balance < file_lenth:
            return Response(status_code='Не хватает баланса')

        # Сделать запись об обработки в Postgre
        await db.execute(insert(AnalysisProcess).values(user_id=user_id, file_id=file_id, file_lenth=file_lenth,
                                                        create_dttm=datetime.datetime.now(), proc_id=uuid4()))
        await db.commit()


        # Транскрибировать/анализировать файл
        asyncio.sleep(10)
        # analysed = analyse_file() # ToDo Сейчас заглушка

        # # Изменить состояние баланса пользователя
        await db.execute(
                update(UserBalance)
                .where(UserBalance.user_id == UUID(user_id))
                .values(balance=new_balance)
                )
        # Удалить запись из analysys_process
        await db.execute(
             delete(AnalysisProcess)
             .where((AnalysisProcess.user_id == UUID(user_id)) & (AnalysisProcess.file_id == UUID(file_id)))
         )
     # Комит обоих операций
        await db.commit()
    return Response(status_code='SUCCESS')
