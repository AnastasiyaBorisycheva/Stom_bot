from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Contact, Message, ReplyKeyboardRemove

from db.session import AsyncSessionLocal
from keyboards.contact import get_phone_keyboard
from repositories import ContactRepository

router = Router()

# Словарь для сопоставления текста кнопки с ответом
PROBLEM_RESPONSES = {
    "ВНЧС": "Вы выбрали тему ВНЧС. Здесь будет тест и информация.",
    "Прикус": "Вы выбрали тему Прикус. Здесь будет тест и информация.",
    "Стираемость зубов": "Вы выбрали тему Стираемость зубов. Здесь будет тест и информация.",
    "Зубы мудрости": "Вы выбрали тему Зубы мудрости. Здесь будет тест и информация.",
    "Записаться к врачу": "Оставьте ваш номер телефона, и мы свяжемся с вами для записи."
}


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


@router.message(F.in_(list(PROBLEM_RESPONSES.keys())))
async def handle_menu_choice(message: Message):
    """Обрабатывает нажатие на кнопки главного меню"""

    choice = message.text
    response = PROBLEM_RESPONSES.get(choice, "Пожалуйста, выберите пункт из меню.")

    await message.answer(response)
