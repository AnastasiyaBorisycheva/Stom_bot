from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (Contact, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)

from ..db.session import AsyncSessionLocal
from ..keyboards.contact import get_phone_keyboard
from ..keyboards.main_menu import get_main_menu_keyboard
from ..keyboards.test_keyboards import (APPOINTMENT_BUTTON, MENU_BUTTON,
                                        get_test_keyboard)
from ..messages.vncs import VNCS_MESSAGES
from ..repositories import ContactRepository, EventRepository, StateRepository
from ..states.user_states import UserStates
from ..utils.message_sender import send_message_by_config

router = Router()


@router.message(F.text == MENU_BUTTON)
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возвращает в главное меню"""
    await state.clear()
    await message.answer(
        "Вы вернулись в главное меню",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "Узнать про ВНЧС")
async def learn_vncs(message: Message):
    """Отправляет первое обучающее сообщение по ВНЧС"""
    msg_config = VNCS_MESSAGES["vncs_learn_1"]
    await send_message_by_config(message, msg_config)


@router.message(F.text == "ВНЧС")
async def vncs_menu(message: Message):
    """Кнопка ВНЧС ведёт на первое обучающее сообщение"""
    msg_config = VNCS_MESSAGES["vncs_learn_1"]
    await send_message_by_config(message, msg_config)


@router.message(F.text == "Записаться к врачу")
async def request_phone(message: Message):
    """Запрашивает номер телефона у пользователя"""

    # Сначала показываем обычное сообщение
    await message.answer(
        "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
        reply_markup=get_phone_keyboard()
    )


@router.message(F.contact)
async def handle_contact(message: Message):
    """Обрабатывает отправленный контакт (номер телефона)"""

    contact = message.contact
    user_id = message.from_user.id
    phone = contact.phone_number
    first_name = contact.first_name

    # Сохраняем или обновляем
    async with AsyncSessionLocal() as session:
        contact_repo = ContactRepository(session)
        saved = await contact_repo.save_or_update_contact(
            user_id=user_id,
            phone=phone,
            source_step="consultation"
        )

    # Убираем клавиатуру
    await message.answer(
        f"Спасибо, {first_name}! Ваш номер сохранён. Мы свяжемся с вами в ближайшее время.",
        reply_markup=ReplyKeyboardRemove()
    )
