import time

import backoff
import requests
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import NoBrokersAvailable
from core.config import get_settings

config = get_settings()


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        NoBrokersAvailable
    ),
)
def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=config.kafka_host[0]
        )

@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        NoBrokersAvailable
    ),
)
def get_kafka_consumer(
    topic: str = "messages", group_id: str = "echo-messages-to-stdout"
) -> KafkaConsumer:
    return KafkaConsumer(
        topic,
        bootstrap_servers=f"{config.kafka_host[0]}",
        auto_offset_reset="earliest",
        group_id=group_id,
        enable_auto_commit=False,
    )