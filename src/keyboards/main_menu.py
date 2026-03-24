from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура главного меню с выбором проблемы"""

    buttons = [
        [KeyboardButton(text="Записаться к врачу")],
        [KeyboardButton(text="ВНЧС")],
        [KeyboardButton(text="Узнать про ВНЧС")],
        [KeyboardButton(text="Прикус")],
        [KeyboardButton(text="Стираемость зубов")],
        [KeyboardButton(text="Зубы мудрости")],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,  # чтобы кнопки были компактными
        one_time_keyboard=False  # не скрывать после нажатия
    )

    return keyboard
