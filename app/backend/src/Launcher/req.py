from requests import get
from config import REF


def go():
    """Запускает скрипт для запуска детекции"""
    print("Hello")


def start():
    """Проверяет состояние запроса на запуск детекции"""
    start_detection = get(f"{REF}start_detection")
    if start_detection.status_code == 200:
        return go()
