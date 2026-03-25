import os
import re

from aiogram.types import (FSInputFile, InlineKeyboardButton,
                           InlineKeyboardMarkup, InputMediaPhoto,
                           InputMediaVideo, Message)
from aiogram.utils.media_group import MediaGroupBuilder


def escape_markdown(text: str) -> str:
    """Экранирует спецсимволы MarkdownV2, но оставляет * и _"""
    # Символы, которые нужно экранировать (все кроме * и _)
    special_chars = r'[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)


async def send_message_by_config(
    message: Message,
    config: dict,
    edit: bool = False,
    parse_mode: str = "MarkdownV2"
):
    """
    Отправляет сообщение на основе конфига.
    config может содержать:
        - text: текст сообщения
        - photo: имя файла (пока локально, потом можно доработать)
        - video: file_id
        - buttons: список кортежей (text, callback_data)
    """
    text = config.get("text", "")
    photo = config.get("photo")
    video = config.get("video")
    buttons = config.get("buttons", [])

    # Если в тексте есть символы форматирования — экранируем их,
    # но не экранируем уже экранированные (чтобы не ломать Markdown)
    if parse_mode == "MarkdownV2":
        # Простая проверка: если текст содержит звёздочки, возможно, это Markdown
        # Но безопаснее всегда экранировать, кроме случаев, когда мы уверены
        # Пока сделаем так: экранируем всё, кроме явных маркдаун-конструкций
        # Для простоты — экранируем всё
        text = escape_markdown(text)

    # Клавиатура
    keyboard = None
    if buttons:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn_text, callback_data=cb_data)]
                for btn_text, cb_data in buttons
            ]
        )

    # Если photo — это локальный файл (не file_id)
    if photo and not photo.startswith("AgAD") and not photo.startswith("http"):
        photo_path = f"src/media/{photo}"
        try:
            photo_file = FSInputFile(photo_path)
            if edit:
                await message.edit_media(
                    InputMediaPhoto(media=photo_file, caption=text, parse_mode=parse_mode),
                    reply_markup=keyboard
                )
            else:
                await message.answer_photo(
                    photo_file, caption=text, parse_mode=parse_mode, reply_markup=keyboard
                )
        except FileNotFoundError:
            # Файла нет — отправляем текст
            if edit:
                await message.edit_text(text, parse_mode=parse_mode, reply_markup=keyboard)
            else:
                await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)
    elif video:
        # Видео пока отключено, отправляем текст
        if edit:
            await message.edit_text(text, parse_mode=parse_mode, reply_markup=keyboard)
        else:
            await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)
    else:
        # Только текст
        if edit:
            await message.edit_text(text, parse_mode=parse_mode, reply_markup=keyboard)
        else:
            await message.answer(text, parse_mode=parse_mode, reply_markup=keyboard)
