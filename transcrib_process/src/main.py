import asyncio
import datetime
import json
from uuid import UUID, uuid4


from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import select, update, delete, insert
from config import get_settings

from kafka_config import get_kafka_consumer, get_kafka_producer
from models import UserBalance, AnalysisProcess
from postgres import async_session
from schemas import Response

config = get_settings()
consumer = get_kafka_consumer(topic=config.topic_name[0], group_id=config.topic_name[0])
producer = get_kafka_producer()


async def main(
    consumer: KafkaConsumer,
    producer: KafkaProducer
):
    """Запускает транскрибацию файла, сообщение с которым лежит в Кафке"""
    # Прочитали сообщение из Кафки
    message = consumer.poll(max_records=1)

    file_id = message['file_id']
    user_id = message['user_id']
    file_lenth = message['file_lenth']
    # Получили доступный баланс пользователя
    async with async_session() as db:
        balance_data = await db.execute(select(UserBalance).where(UserBalance.user_id == UUID(user_id))) #get_balance(user_id)
        in_process = await db.execute(select(AnalysisProcess).where(AnalysisProcess.user_id == UUID(user_id)))

        new_balance = balance_data.scalars().first().balance - in_process.scalars().first().file_lenth


        if new_balance < file_lenth:
            message_kafka = {'file_id': str(file_id), 'user_id': str(user_id), 'status_code': 404,
                             'result': 'Не хватает баланса'}
            # Записываем в топик результата обработки
            producer.send(
                topic='for_transcrib',
                value=json.dumps(message_kafka).encode(),
                key=str(message.file_id).encode(),
                headers=[('user_id', str(message.file_id).encode())]
            )
            response = Response(status_code='Не хватает баланса')
            return response

        # Сделать запись об обработки в Postgre
        await db.execute(insert(AnalysisProcess).values(user_id=user_id, file_id=file_id, file_lenth=file_lenth,
                                                        create_dttm=datetime.datetime.now(), proc_id=uuid4()))
        await db.commit()


        # Транскрибировать/анализировать файл
        asyncio.sleep(10)
        # analysed = analyse_file() # ToDo Сейчас заглушка

        # # Изменить состояние баланса пользователя
        message = f'Сообщение данной длинны может быть транскрибировано. Оставшийся баланс {new_balance} минут'
        # Записываем в топик результат обработки
        message_kafka = {'file_id': str(file_id), 'user_id': str(user_id), 'status_code': 200,
                         'result': message}
        producer.send(
            topic='for_transcrib',
            value=json.dumps(message_kafka).encode(),
            key=str(message.file_id).encode(),
            headers=[('user_id', str(message.file_id).encode())]
        )

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

if __name__ == "__main__":
    asyncio.run(main(consumer=consumer, producer=producer))
