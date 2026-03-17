# src/handlers/start.py

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload  # для меток

from db.session import AsyncSessionLocal
from messages import MESSAGES
from repositories import UserRepository
from utils.time_utils import format_datetime  # пригодится для отладки
from utils.time_utils import format_date

router = Router()


def parse_start_payload(text: str) -> tuple[str | None, str | None]:
    """
    Разбирает payload из команды /start.
    Возвращает (source, problem)

    Примеры:
    /start VK_TMJ -> ("VK", "TMJ")
    /start INST_WEAR -> ("INST", "WEAR")
    /start просто -> (None, None)
    """
    parts = text.split()
    if len(parts) < 2:
        return None, None

    payload = parts[1].strip()
    if '_' in payload:
        source, problem = payload.split('_', 1)
        return source, problem
    return payload, None  # если без подчёркивания, сохраняем как source


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""

    # Получаем данные пользователя из Telegram
    tg_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Разбираем метки (place params)
    source, problem = parse_start_payload(message.text or "")

    # Логируем для отладки
    print(f"🔥 /start от {tg_id} (@{username}) | source: {source}, problem: {problem}")

    # Работа с БД
    async with AsyncSessionLocal() as session:
        user_repo = UserRepository(session)

        # Сохраняем или обновляем пользователя
        user, created = await user_repo.get_or_create(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            source=source  # передаём источник
        )

        # Если есть проблема, можно сохранить в отдельную таблицу
        # (позже сделаем)

        # Приветствие
        if created:
            # Новый пользователь
            text = MESSAGES["welcome_new"].format(name=first_name)
        else:
            # Старый пользователь
            first_date = format_date(user.first_seen)
            text = MESSAGES["welcome_old"].format(
                name=first_name,
                first_date=first_date
            )

        await message.answer(text)
