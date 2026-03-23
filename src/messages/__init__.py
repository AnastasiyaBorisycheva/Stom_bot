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
