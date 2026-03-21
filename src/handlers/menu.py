from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (Contact, KeyboardButton, Message,
                           ReplyKeyboardMarkup, ReplyKeyboardRemove)

from db.session import AsyncSessionLocal
from keyboards.contact import get_phone_keyboard
from keyboards.main_menu import get_main_menu_keyboard
from keyboards.test_keyboards import (APPOINTMENT_BUTTON, MENU_BUTTON,
                                      get_test_keyboard)
from repositories import ContactRepository, StateRepository, EventRepository
from states.user_states import UserStates
from tests import TESTS, get_test_by_button


router = Router()


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


@router.message(F.text.in_(list(TESTS.keys())))
async def start_test(message: Message, state: FSMContext):
    """Универсальный старт любого теста"""

    test = get_test_by_button(message.text)
    if not test:
        return

    # Сохраняем в контексте
    await state.update_data(test_name=test.name, step=1, answers={})
    await state.set_state(UserStates.test_active)

    # Сохраняем в БД (опционально)
    async with AsyncSessionLocal() as session:
        state_repo = StateRepository(session)
        await state_repo.set_state(
            user_id=message.from_user.id,
            state_name="test_active",
            data={"test": test.name, "step": 1}
        )

    # Первый вопрос
    first_q = test.questions[0]
    keyboard = get_test_keyboard(first_q['buttons'])

    await message.answer(first_q['text'], reply_markup=keyboard)


@router.message(UserStates.test_active, F.text)
async def handle_test_answer(message: Message, state: FSMContext):
    """Обрабатывает ответы в тесте, включая выход и запись"""

    # Обработка нажатия "Главное меню"
    if message.text == MENU_BUTTON:
        await state.clear()
        async with AsyncSessionLocal() as session:
            state_repo = StateRepository(session)
            await state_repo.clear_state(message.from_user.id)

        await message.answer(
            "Вы вернулись в главное меню.",
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Обработка нажатия "Записаться к врачу"
    if message.text == APPOINTMENT_BUTTON:
        # Сохраняем текущие ответы (на всякий случай)
        data = await state.get_data()

        # Сохранить частичный результат в events
        async with AsyncSessionLocal() as session:
            event_repo = EventRepository(session)
            await event_repo.add_event(
                user_id=message.from_user.id,
                event_name="test_interrupted",
                event_data={
                    "test_name": data.get('test_name'),
                    "step": data.get('step', 1),
                    "answers": data.get('answers', {})
                }
            )

        await state.clear()
        async with AsyncSessionLocal() as session:
            state_repo = StateRepository(session)
            await state_repo.clear_state(message.from_user.id)

        # Запрашиваем телефон
        from keyboards.contact import get_phone_keyboard
        await message.answer(
            "Хорошо. Оставьте ваш номер телефона, и мы свяжемся с вами для записи.",
            reply_markup=get_phone_keyboard()
        )
        return

    data = await state.get_data()
    test_name = data.get('test_name')
    step = data.get('step', 1)
    answers = data.get('answers', {})

    # Находим тест по названию
    test = None
    for t in TESTS.values():
        if t.name == test_name:
            test = t
            break

    if not test:
        await state.clear()
        return

    # Сохраняем ответ
    answers[step] = message.text
    await state.update_data(answers=answers, step=step + 1)

    # Проверяем, есть ли следующий вопрос
    if step < len(test.questions):
        next_q = test.questions[step]  # следующий вопрос
        keyboard = get_test_keyboard(next_q['buttons'])
        await message.answer(next_q['text'], reply_markup=keyboard)
    else:
        # Тест окончен
        result = test.get_result(answers)

        # Сохраняем результат в events
        async with AsyncSessionLocal() as session:
            event_repo = EventRepository(session)
            await event_repo.add_event(
                user_id=message.from_user.id,
                event_name=f"test_completed_{test.name}",
                event_data={
                    "test_name": test.name,
                    "answers": answers,
                    "result": result
                }
            )

            state_repo = StateRepository(session)
            await state_repo.clear_state(message.from_user.id)

        await state.clear()

        # Возвращаем главное меню
        await message.answer(
            result,
            reply_markup=get_main_menu_keyboard()
        )