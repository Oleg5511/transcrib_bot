from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from core.config import get_settings
from kafka_service.kafka_config import get_kafka_consumer

api_hash = "8c86aa0ee784f88a2e2b2f5fbc084f0b"
api_id = "15519192"

config = get_settings()
consumer = get_kafka_consumer(topic=config.topic_name[0], group_id=config.topic_name[0])

def all_message(client: Client, message: Message, consumer):
    """Функция вычитывает топик кафку и отсылает сообщение пользователю"""

    message = consumer.poll(max_records=1)

with Client(name="rechka", api_hash=api_hash, api_id=api_id) as app:
    app.send_message("me", "Это я бот")
    app.add_handler(MessageHandler(all_message()))

