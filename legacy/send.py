import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaVideo

def sm(bot, chat_id, text=None, video_id=None, photo=None, buttons=None, markdown=True):
    # Создаем клавиатуру, если кнопки есть
    keyboard = None
    if buttons:
        keyboard = InlineKeyboardMarkup()
        for btn_text, btn_id in buttons:
            keyboard.add(InlineKeyboardButton(text=btn_text, callback_data=btn_id))

    def contains_markdown(s):
        # Простая проверка на наличие базовых markdown-символов
        markdown_chars = ['*', '_', '`', '[', ']','~']
        return markdown if not markdown else any(ch in s for ch in markdown_chars)

    # Отправляем согласно приоритету: видео, затем фото, затем текст
    if video_id:
        msg = bot.send_video(chat_id, video_id, caption=text or '', reply_markup=keyboard, parse_mode='Markdown' if text and contains_markdown(text) else None)
    elif photo:
        # Отправляем сжатую фотографию
        #with open(photo, 'rb') as photo_file:
        msg = bot.send_photo(chat_id, photo, caption=text or '', reply_markup=keyboard, parse_mode='Markdown' if text and contains_markdown(text) else None)
    else:
        if contains_markdown(text):
            msg = bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
        else:
            msg = bot.send_message(chat_id, text, reply_markup=keyboard)
    return msg.message_id

def edit_last_message(bot, chat_id, message_id, text=None, video_id=None, photo=None, buttons=None, markdown=True):
    try:
        keyboard = None
        if buttons:
            keyboard = InlineKeyboardMarkup()
            for btn_text, btn_id in buttons:
                keyboard.add(InlineKeyboardButton(text=btn_text, callback_data=btn_id))

        def contains_markdown(s):
            markdown_chars = ['*', '_', '`', '[', ']', '~']
            if not markdown:
                return markdown
            return any(ch in s for ch in markdown_chars) if s else False

        parse_mode = 'Markdown' if text and contains_markdown(text) else None

        if video_id:
            media = InputMediaVideo(media=video_id, caption=text or '', parse_mode=parse_mode)
            msg = bot.edit_message_media(media, chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        elif photo:
            #bot.delete_message(chat_id, message_id)
            #with open(photo, 'rb') as photo_file:
                #photo_data = photo_file.read()
            media = InputMediaPhoto(media = photo, caption=text or '', parse_mode=parse_mode)
            msg = bot.edit_message_media(media, chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
            #msg = bot.send_photo(chat_id, photo_data, caption=text or '', parse_mode=parse_mode, reply_markup=keyboard)
        else:
            try:
                msg = bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=keyboard, parse_mode=parse_mode)
            except:
                bot.delete_message(chat_id, message_id)
                if contains_markdown(text):
                    msg = bot.send_message(chat_id, text, reply_markup=keyboard, parse_mode='Markdown')
                else:
                    msg = bot.send_message(chat_id, text, reply_markup=keyboard)
        return msg.message_id
    except:
        pass
