from .vncs import VNCSTest
from .bite import BiteTest
from .wear import WearTest
from .wisdom import WisdomTest

# Словарь: текст кнопки -> объект теста
TESTS = {
    "ВНЧС": VNCSTest(),
    "Прикус": BiteTest(),
    "Стираемость зубов": WearTest(),
    "Зубы мудрости": WisdomTest(),
}


def get_test_by_button(button_text: str):
    """Возвращает тест по тексту кнопки"""
    return TESTS.get(button_text)
