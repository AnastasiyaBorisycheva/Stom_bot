# src/messages/__init__.py

from .vncs import VNCS_MESSAGES
from .wisdom import WISDOM_MESSAGES
from .wear import WEAR_MESSAGES
from .bite import BITE_MESSAGES

# Ключи, которые НЕ должны попадать в ALL_MESSAGES (тесты, служебные)
TEST_KEYS = {
    # ВНЧС
    "test_vncs_q1", "test_vncs_q2", "test_vncs_q3", "test_vncs_q4", "test_vncs_q5",
    # Зубы мудрости
    "wisdom_teeth_test_q1", "wisdom_teeth_test_q2", "wisdom_teeth_test_q3",
    "wisdom_teeth_test_q4", "wisdom_teeth_test_q5",
    # Стираемость
    "wear_test_q1", "wear_test_q2", "wear_test_q3", "wear_test_q4", "wear_test_q5", "wear_test_q6",
    # Прикус (тест на брекеты)
    "bite_braces_q1", "bite_braces_q2", "bite_braces_q3", "bite_braces_q4", "bite_braces_q5",
}

# Объединяем все сообщения
ALL_MESSAGES = {
    **VNCS_MESSAGES,
    **WISDOM_MESSAGES,
    **WEAR_MESSAGES,
    **BITE_MESSAGES,
}

# Удаляем ключи тестов (чтобы они не перехватывались educational.py)
for key in TEST_KEYS:
    ALL_MESSAGES.pop(key, None)

# Базовые сообщения (приветствия и т.д.)
MESSAGES = {
    "welcome_new": "Приветствуем Вас в Центре цифровой стоматологии МАРТИ.\nПодскажите, пожалуйста, что Вас беспокоит?",
    "welcome_old": "С возвращением, {name}! Вы уже обращались к нам {first_date}. Можем продолжить или начать сначала."
}

# Сообщение после записи
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

__all__ = [
    "ALL_MESSAGES",
    "MESSAGES",
    "CONSULTATION_MESSAGE",
    "VNCS_MESSAGES",
    "WISDOM_MESSAGES",
    "WEAR_MESSAGES",
    "BITE_MESSAGES"
]
