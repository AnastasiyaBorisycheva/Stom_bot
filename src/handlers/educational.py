from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..keyboards.contact import get_phone_keyboard
from ..keyboards.main_menu import get_main_menu_keyboard
from ..messages import ALL_MESSAGES
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


@router.callback_query(F.data.in_(ALL_MESSAGES.keys()))
async def handle_educational_callback(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатия на кнопки образовательных сообщений"""
    msg_id = callback.data
    msg_config = ALL_MESSAGES.get(msg_id)
    if not msg_config:
        await callback.answer("Сообщение не найдено")
        return

    await state.set_state(UserStates.education)

    # Проверяем, можно ли редактировать
    original_message = callback.message
    can_edit = False
    if original_message.photo or original_message.video:
        # Если исходное сообщение содержит медиа — не редактируем
        can_edit = False
    elif not msg_config.get("photo") and not msg_config.get("video"):
        # Если и новое сообщение без медиа — можно редактировать
        can_edit = True
    await send_message_by_config(
        callback.message,
        msg_config,
        edit=can_edit  # редактируем текущее сообщение
    )

    await callback.answer()
