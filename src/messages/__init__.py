# src/messages/__init__.py

# Базовые сообщения (приветствия, общие)
MESSAGES = {
    "welcome_new": "Привет, {name}!\n\nЯ бот стоматологии. Помогу подобрать подходящего врача и записаться на приём.",
    "welcome_old": "С возвращением, {name}!\n\nВы уже обращались к нам {first_date}. Можем продолжить или начать сначала."
}

# Импортируем конфиги для воронок (пока пустые, заполним позже)
from .vncs import VNCS_MESSAGES
from .wisdom import WISDOM_MESSAGES
from .wear import WEAR_MESSAGES
from .bite import BITE_MESSAGES

__all__ = ["MESSAGES", "VNCS_MESSAGES", "WISDOM_MESSAGES", "WEAR_MESSAGES", "BITE_MESSAGES"]


CONSULTATION_MESSAGE = {
    "text": """Добрый день! Спасибо, что выбрали нашу цифровую стоматологию «МАРТИ» ♥️
Мы уже получили Вашу заявку и свяжемся с Вами в течение 30 минут.

С уважением, команда цифровой стоматологии «МАРТИ»
Адрес:
📍 [г.Москва, 3-й Павелецкий проезд, 3](https://yandex.ru/maps/org/marti/61375681640?si=h89wwjg7cpvk5tak82bgkq0ar8)
📞 +7 (495) 003-14-53
@stommarti""",
    "buttons": [
        ("🔘 Главное меню", "start_main")
    ]
}