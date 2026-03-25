from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🔘 ВНЧС", callback_data="vncs_start_f")],
        [InlineKeyboardButton(text="🔘 Прикус", callback_data="bite_start")],
        [InlineKeyboardButton(text="🔘 Стираемость зубов", callback_data="wear_start")],
        [InlineKeyboardButton(text="🔘 Зубы мудрости", callback_data="wisdom_teeth_start")],
        [InlineKeyboardButton(text="🔘 Записаться к врачу", callback_data="consultation")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)