import json
from http import HTTPStatus
from fastapi import Depends, HTTPException
# from fastapi.encoders import jsonable_encoder
from kafka import KafkaProducer
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.exc import IntegrityError
from functools import lru_cache
import requests
from helpers.helpers import send_for_transcrib
from kafka_config.kafka_config import get_kafka_producer
from schemas.schemas import FileInfo, Response, ForTranscrib
# from schemas.schemas_entity import UserInDB
from core.config import get_settings
from db.postgres import get_session
# from models.models import File
from services.base_serv import BaseService
import backoff
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable


config = get_settings()
producer = get_kafka_producer()

def init_transcrib( message, producer=producer) -> Response:
    """Функция отправляет сообщение в кафку"""

    message_kafka = {'file_id': str(message.file_id), 'user_id': str(message.user_id),
                     'file_lenth': message.file_lenth}
    producer.send(
        topic='for_transcrib',
        value=json.dumps(message_kafka).encode(),
        key=str(message.file_id).encode(),
        headers=[('user_id', str(message.file_id).encode())]
    )

    response = Response(status_code='Удачно ёмаё')
    return response

message = ForTranscrib(user_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                       file_id="3fa85f64-5717-4562-b3fc-2c963f66afa6", file_lenth=1)

r = init_transcrib(message, producer=producer)
print(r)
# class TranscribService(BaseService):
#     """Сервис транскрибации"""
#
#     def __init__(self, session: AsyncSession):
#         self.session = session
#
#     async def start_transcrib(self, message, producer: KafkaProducer) -> Response:
#         """Функция отправляет сообщение в кафку"""
#
#         message_kafka = {'file_id': message.file_id, 'user_id': message.user_id,
#                          'file_lenth': message.file_lenth}
#         producer.send(
#             topic='for_transcrib',
#             value=json.dumps(message_kafka).encode(),
#             key=message['user_id'].encode(),
#             headers=[('user_id', message['user_id'].encode())]
#         )
#
#         response = Response(status_code='Удачно ёмаё')
#         return response
#
#
# @lru_cache
# def get_transcrib_service(
#     session: AsyncSession = Depends(get_session),
# ) -> TranscribService:
#     """Возвращает синглтон сервиса"""
#     return TranscribService(session=session)
