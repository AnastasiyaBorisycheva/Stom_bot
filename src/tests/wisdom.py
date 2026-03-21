from .base import BaseTest
from typing import Dict


class WisdomTest(BaseTest):
    
    @property
    def name(self) -> str:
        return "ВНЧС"
    
    @property
    def start_state(self) -> str:
        return "vncs_test"
    
    @property
    def questions(self):
        return [
            {'text': 'Чувствуете ли вы щелчки или хруст при открывании рта?', 'buttons': ['Да', 'Нет']},
            {'text': 'Бывает ли головная боль, которая начинается от виска?', 'buttons': ['Да', 'Нет']},
            {'text': 'Чувствуете ли вы напряжение в челюсти по утрам?', 'buttons': ['Да', 'Нет']},
            {'text': 'Слышите ли вы свист или шум в ушах?', 'buttons': ['Да', 'Нет']},
            {'text': 'Бывает ли сложно широко открыть рот?', 'buttons': ['Да', 'Нет']}
        ]
    
    def get_result(self, answers: Dict[int, str]) -> str:
        if any(answer == "Да" for answer in answers.values()):
            return ("По вашим ответам есть признаки нарушения ВНЧС. "
                    "Рекомендуем записаться на консультацию к гнатологу.")
        return ("По вашим ответам явных нарушений не видно. "
                "Если вас что-то беспокоит, вы всегда можете записаться на консультацию.")