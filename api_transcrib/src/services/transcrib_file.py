from sqlalchemy.ext.asyncio import AsyncSession
from kafka import KafkaConsumer
from sqlalchemy import select, update, delete
# from helpers.helpers import get_file_lenth, send_from_transcrib, analyse_file, send_to_user
from core.config import get_settings
from kafka_config.kafka_config import get_kafka_consumer
from models.models import AnalysisProcess, UserBalance
from schemas.schemas import FromTranscrib

config = get_settings()
consumer = get_kafka_consumer(topic=config.topic_name[0], group_id=config.topic_name[0])

def transcrib_file(
    consumer: KafkaConsumer,
    # db: AsyncSession
):
    """Запускает транскрибацию файла, сообщение с которым лежит в Кафке"""
    print('*********')
    # Прочитали сообщение из Кафки
    message = consumer.poll(max_records=1)
    print('++++++', message)
    # file_id = message['file_id']  # ToDo Поправить формат данных который приходит из кафки
    # user_id = message['file_id']

while True:
    transcrib_file(consumer=consumer)

    # # Получили длину файла
    # file_lenth = get_file_lenth(file_id)
    #
    # # Получили доступный баланс пользователя
    # balance_data = await db.execute(select(UserBalance).where(UserBalance.balance == user_id) #get_balance(user_id)
    # in_process = await db.execute(select(AnalysisProcess).where(AnalysisProcess.user_id == user_id)
    # new_balance = balance_data.balance-in_process.file_lenth
    #
    # if new_balance < file_lenth:
    #     message = FromTranscrib(user_id = user_id,
    #                             file_id=file_id,
    #                             status_code=404,
    #                             result='Баланс меньше необходимого')
    #     # Записываем в топик результата обработки
    #         send_from_transcrib(message)
    #
    # # Сделать запись об обработки в Postgre
    # await db.execute(AnalysisProcess.insert().values(user_id = user_id, file_id=file_id,file_lenth=file_lenth))
    #
    # # Транскрибировать/анализировать файл
    # analysed = analyse_file() # ToDo Сейчас заглушка
    #
    # # Отправить сообщение пользователю
    # send_to_user(analysed) # ToDo Сейчас заглушка
    #
    #
    # # Изменить состояние баланса пользователя
    # try:
    # await db.execute(
    #         update(UserBalance)
    #         .where(UserBalance.user_id == user_id)
    #         .values(balance=new_balance)
    #     )
    # # Удалить запись из analysys_process
    # await db.execute(
    #         delete(AnalysisProcess)
    #         .where((AnalysisProcess.user_id == user_id) & (AnalysisProcess.file_id == file_id))
    #     )
    # # Комит обоих операций
    # await db.commit()
