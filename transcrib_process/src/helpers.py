import json
from kafka import KafkaProducer
from config import get_settings
from http import HTTPStatus

config = get_settings()


# def send_for_transcrib(
#         producer: KafkaProducer,
#         message
#     ):
#     """Функция отправляет сообщение в Кафку в топик to_transcrib"""
#     message_kafka = {'file_id': message['file_id'], 'user_id': message['user_id'], 'file_lenth':message['file_lenth']}
#     producer.send(
#                 topic='for_transcrib',
#                 value=json.dumps(message_kafka).encode(),
#                 key=message['user_id'].encode(),
#                 headers=[('user_id', message['user_id'].encode())]
#             )
#     return HTTPStatus.OK

def send_from_transcrib(
        producer: KafkaProducer,
        message
    ):
    """Функция отправляет сообщение в Кафку в топик from_transcrib"""
    message_kafka = {'user_id': message['user_id'], 'file_id': message['file_id'],
                     'status_code': message['status_code'], 'result': message['result']}
    producer.send(
                topic='from_transcrib',
                value=json.dumps(message_kafka).encode(),
                key=message['user_id'].encode(),
                headers=[('user_id', message['user_id'].encode())]
            )
    return HTTPStatus.OK
