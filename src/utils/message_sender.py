from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InputMediaPhoto, InputMediaVideo


async def send_message_by_config(
    message: Message,
    config: dict,
    edit: bool = False
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

    # Клавиатура
    keyboard = None
    if buttons:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn_text, callback_data=cb_data)]
                for btn_text, cb_data in buttons
            ]
        )

    # Отправляем с учётом медиа
    if False and video:  # Видео временно отключено
        if edit:
            await message.edit_media(
                media=InputMediaVideo(media=video, caption=text),
                reply_markup=keyboard
            )
        else:
            await message.answer_video(video, caption=text, reply_markup=keyboard)
    elif photo and False:  # Фото временно отключены
        if edit:
            await message.edit_media(
                media=InputMediaPhoto(media=photo, caption=text),
                reply_markup=keyboard
            )
        else:
            await message.answer_photo(photo, caption=text, reply_markup=keyboard)
    else:
        if edit:
            await message.edit_text(text, reply_markup=keyboard)
        else:
            await message.answer(text, reply_markup=keyboard)
