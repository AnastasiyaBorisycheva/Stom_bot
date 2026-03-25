from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Служебные кнопки
MENU_BUTTON = "🔘 Главное меню"
APPOINTMENT_BUTTON = "🔘 Записаться к врачу"


def get_test_keyboard(buttons: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт клавиатуру для теста с основными кнопками и служебными внизу.
    """
    # Основные кнопки (вопросы)
    main_buttons = [[KeyboardButton(text=b) for b in buttons]]

    # Служебные кнопки
    service_buttons = [
        [KeyboardButton(text=APPOINTMENT_BUTTON)],
        [KeyboardButton(text=MENU_BUTTON)]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=main_buttons + service_buttons,
        resize_keyboard=True,
        one_time_keyboard=False  # не скрывать после нажатия
    )
    return keyboard
