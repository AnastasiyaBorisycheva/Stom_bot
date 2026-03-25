from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from ..db.session import AsyncSessionLocal
from ..keyboards.contact import get_phone_keyboard
from ..keyboards.main_menu import get_main_menu_keyboard
from ..messages.vncs import VNCS_MESSAGES
from ..repositories import ContactRepository, EventRepository, StateRepository
from ..states.user_states import UserStates
from ..utils.message_sender import send_message_by_config

router = Router()


@router.callback_query(F.data == "start_main")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    """Возвращает пользователя в главное меню"""
    await state.set_state(UserStates.main_menu)
    await state.clear()  # очищаем все данные FSM

    # Убираем инлайн-клавиатуру и отправляем новое сообщение с главным меню
    await callback.message.delete()
    await callback.message.answer(
        "Вы вернулись в главное меню",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "consultation")
async def consultation_request(callback: CallbackQuery, state: FSMContext):
    """Запись на консультацию — запрос телефона"""
    await state.set_state(UserStates.consultation)
    await callback.message.delete()
    await callback.message.answer(
        "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
        reply_markup=get_phone_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.in_(VNCS_MESSAGES.keys()))
async def handle_educational_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатия на кнопки образовательных сообщений"""
    msg_id = callback.data
    msg_config = VNCS_MESSAGES[msg_id]

    await state.set_state(UserStates.education)

    await send_message_by_config(
        callback.message,
        msg_config,
        edit=True  # редактируем текущее сообщение
    )

    await callback.answer()
