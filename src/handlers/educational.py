from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from src.messages.vncs import VNCS_MESSAGES
from src.states.user_states import UserStates
from src.utils.message_sender import send_message_by_config

router = Router()

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
