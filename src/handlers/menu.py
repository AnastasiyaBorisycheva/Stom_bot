from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardRemove

from ..db.session import AsyncSessionLocal
from ..messages import CONSULTATION_MESSAGE
from ..repositories import ContactRepository
from ..utils.message_sender import send_message_by_config

router = Router()


@router.message(F.contact)
async def handle_contact(message: Message):
    """Обрабатывает отправленный контакт (номер телефона)"""

    contact = message.contact
    user_id = message.from_user.id
    phone = contact.phone_number

    # Сохраняем или обновляем
    async with AsyncSessionLocal() as session:
        contact_repo = ContactRepository(session)
        await contact_repo.save_or_update_contact(
            user_id=user_id,
            phone=phone,
            source_step="consultation"
        )

    # Отправляем финальное сообщение
    await send_message_by_config(
        message,
        CONSULTATION_MESSAGE,
        edit=False  # новое сообщение, не редактируем
    )
