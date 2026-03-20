from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура с кнопкой для отправки телефона"""

    button = KeyboardButton(
        text="Отправить номер телефона",
        request_contact=True  # Telegram запросит разрешение и отправит контакт
    )

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button]],
        resize_keyboard=True,
        one_time_keyboard=True  # скроется после нажатия
    )

    return keyboard
