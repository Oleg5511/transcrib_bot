import json
from kafka import KafkaProducer
from core.config import get_settings
from http import HTTPStatus

config = get_settings()


def send_for_transcrib(
        producer: KafkaProducer,
        message
    ):
    """Функция отправляет сообщение в Кафку в топик to_transcrib"""
    message_kafka = {'file_id': message['file_id'], 'user_id': message['user_id'], 'file_lenth':message['file_lenth']}
    producer.send(
                topic='for_transcrib',
                value=json.dumps(message_kafka).encode(),
                key=message['user_id'].encode(),
                headers=[('user_id', message['user_id'].encode())]
            )
    return HTTPStatus.OK


# def get_file_lenth(file_id):
#     """Функция получает длину файла по dile_id"""
#     pass
#
#
# def get_balance(user_id):
#     """Функция получается баланс пользователя """
#     pass
#
# def send_from_transcrib(
#         producer: KafkaProducer,
#         message
#     ):
#     """Функция отправляет сообщение в Кафку в топик from_transcrib"""
#     message_kafka = {'user_id': message['user_id'], 'file_id': message['file_id'],
#                      'status_code': message['status_code'], 'result': message['result']}
#     producer.send(
#                 topic='from_transcrib',
#                 value=json.dumps(message_kafka).encode(),
#                 key=message['user_id'].encode(),
#                 headers=[('user_id', message['user_id'].encode())]
#             )
#     return HTTPStatus.OK
#
# def analyse_file():
#     pass
#
# def send_to_user(analysed):
#     pass
#
# def change_balance(user_id, balance_id):
#     await db.execute(
#         update(UserBalance)
#         .where(TokenBase.jti == uuid.UUID(refresh_jti))
#         .values(status_code=TokenStatus.cancelled)
#     )
#     await db.commit()
#     pass