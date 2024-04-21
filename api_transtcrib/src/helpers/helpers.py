import json
from kafka import KafkaProducer
from core.config import get_settings
from http import HTTPStatus

config = get_settings()


def send_to_transcrib(
        producer: KafkaProducer,
        message
    ):
    """Функция отправляет сообщение в Кафку в топик to_transcrib"""
    message_kafka = {'file_id': message['file_id'], 'user_id': message['user_id']}
    producer.send(
                topic='to_transcrib',
                value=json.dumps(message_kafka).encode(),
                key=message['user_id'].encode(),
                headers=[('user_id', message['user_id'].encode())]
            )
    return HTTPStatus.OK

def get_file_lenth(file_id):
    pass


def get_balance(user_id):
    pass

def send_from_transcrib(message):
    pass

def analyse_file():
    pass

def send_to_user(analysed):
    pass



def change_balance(user_id, balance_id):
    pass