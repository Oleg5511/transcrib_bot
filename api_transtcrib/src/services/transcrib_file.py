from sqlalchemy.ext.asyncio import AsyncSession
from kafka import KafkaConsumer

from helpers.helpers import get_file_lenth, get_balance, send_from_transcrib, analyse_file, send_to_user, change_balance
from schemas.schemas import FromTranscrib



def transcrib_file(
    consumer: KafkaConsumer,
    db: AsyncSession
):
    """Запускает транскрибацию файла, сообщение с которым лежит а Кафке"""

    # Прочитали сообщение из Кафки
    message = consumer.poll(max_records=1)
    file_id = message['file_id']  # ToDo Поправить формат данных который приходит из кафки
    user_id = message['file_id']

    # Получили длину файла
    try:
        file_lenth = get_file_lenth(file_id)
    except ОШИБКА:
        raise ОШИБКА

    # Получили доступный баланс пользователя
    try:
        balance = get_balance(user_id)
    except ОШИБКА:
        raise ОШИБКА

    if balance < file_lenth:
        message = FromTranscrib(file_id=file_id,
                                status_code=404,
                                result='Баланс меньше необходимого')
        # Записываем в топик результата обработки (в проде должен быть отдельный топик или очередь)
        try:
            send_from_transcrib(message)
        except ОШИБКА:
            raise ОШИБКА
    # Транскрибировать/анализировать файл
    try:
        analysed = analyse_file()
    except ОШИБКА:
        raise ОШИБКА

    #Отправить сообщение пользователю
    try:
        send_to_user(analysed)
    except ОШИБКА:
        raise ОШИБКА

    #Изменить состояние баланса пользователя и удалить запись из analysys_process
    try:
        change_balance(user_id, balance)
    except ОШИБКА:
        raise ОШИБКА


