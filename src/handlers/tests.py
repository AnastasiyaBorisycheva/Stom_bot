from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from ..db.session import AsyncSessionLocal
from ..messages import (BITE_MESSAGES, VNCS_MESSAGES, WEAR_MESSAGES,
                        WISDOM_MESSAGES)
from ..repositories import EventRepository
from ..states.user_states import UserStates
from ..utils.message_sender import send_message_by_config

router = Router()


@router.callback_query(F.data == "start_test_vncs")
async def start_vncs_test(callback: CallbackQuery, state: FSMContext):
    """Начинает тест ВНЧС"""
    await state.set_state(UserStates.vncs_test)
    await state.update_data(score=0, answers={})

    msg_config = VNCS_MESSAGES["test_vncs_q1"]
    await send_message_by_config(callback.message, msg_config, edit=True)
    await callback.answer()


@router.callback_query(F.data == "start_wisdom_teeth_test")
async def start_wisdom_teeth_test(callback: CallbackQuery, state: FSMContext):
    """Начинает тест Зубы мудрости"""
    await state.set_state(UserStates.wisdom_test)
    await state.update_data(score=0, answers={})

    msg_config = WISDOM_MESSAGES["wisdom_teeth_test_q1"]
    await send_message_by_config(callback.message, msg_config, edit=True)
    await callback.answer()


@router.callback_query(F.data == "bite_braces_q1")
async def start_bite_braces_test(callback: CallbackQuery, state: FSMContext):
    """Начинает тест на брекеты"""
    print("DEBUG: start_bite_braces_test вызван")
    await state.set_state(UserStates.bite_braces_test)
    await state.update_data(score=0, answers={})
    msg_config = BITE_MESSAGES["bite_braces_q1"]
    await send_message_by_config(callback.message, msg_config, edit=True)
    await callback.answer()


@router.callback_query(F.data == "wear_test_q1")
async def start_wear_test(callback: CallbackQuery, state: FSMContext):
    """Начинает тест на стираемость зубов"""
    print("DEBUG: start_wear_test вызван")  # для отладки
    await state.set_state(UserStates.wear_test)
    await state.update_data(score=0, answers={})
    msg_config = WEAR_MESSAGES["wear_test_q1"]
    await send_message_by_config(callback.message, msg_config, edit=False)
    await callback.answer()


@router.callback_query(UserStates.vncs_test)
async def handle_vncs_test(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает ответы в тесте ВНЧС"""
    callback_data = callback.data

    data = await state.get_data()
    score = data.get("score", 0)
    answers = data.get("answers", {})

    if callback_data.startswith("test_vncs_q"):
        parts = callback_data.split("_")
        if len(parts) >= 4:
            question_part = parts[2]
            question_num = int(question_part[1:])
            points = int(parts[3])

            answers[f"q{question_num}"] = points
            score += points
            await state.update_data(score=score, answers=answers)

            if question_num < 5:
                next_q = f"test_vncs_q{question_num + 1}"
                msg_config = VNCS_MESSAGES[next_q]
                # Отправляем новое сообщение
                await send_message_by_config(callback.message, msg_config, edit=False)
                
                # Опционально: удаляем предыдущее (чтобы не захламлять)
                await callback.message.delete()
            else:
                await state.clear()

                if score <= 2:
                    result_key = "result_vncs_normal"
                elif score <= 5:
                    result_key = "result_vncs_overload"
                elif score <= 7:
                    result_key = "result_vncs_dysfunction"
                else:
                    result_key = "result_vncs_pathology"

                result_config = VNCS_MESSAGES[result_key]
                await send_message_by_config(callback.message, result_config, edit=True)

                async with AsyncSessionLocal() as session:
                    event_repo = EventRepository(session)
                    await event_repo.add_event(
                        user_id=callback.from_user.id,
                        event_name="vncs_test_completed",
                        event_data={"score": score, "answers": answers, "result": result_key}
                    )

    elif callback_data == "start_main":
        await state.clear()
        from ..keyboards.main_menu import get_main_menu_keyboard
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

    elif callback_data == "consultation":
        from ..keyboards.contact import get_phone_keyboard
        await state.set_state(UserStates.consultation)
        await callback.message.delete()
        await callback.message.answer(
            "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
            reply_markup=get_phone_keyboard()
        )

    await callback.answer()


@router.callback_query(UserStates.wisdom_test)
async def handle_wisdom_test(callback: CallbackQuery, state: FSMContext):
    callback_data = callback.data

    data = await state.get_data()
    score = data.get("score", 0)
    answers = data.get("answers", {})

    if callback_data.startswith("wisdom_teeth_test_q"):
        # Парсим callback_data: wisdom_teeth_test_q{num}_{points}
        parts = callback_data.split("_")
        if len(parts) >= 5:
            question_part = parts[3]  # 'q1'
            question_num = int(question_part[1:])  # 1
            points = int(parts[4])  # 2, 1, 0

            answers[f"q{question_num}"] = points
            score += points
            await state.update_data(score=score, answers=answers)

            if question_num < 5:
                next_q = f"wisdom_teeth_test_q{question_num + 1}"
                msg_config = WISDOM_MESSAGES[next_q]
                # Сначала отправляем новое, потом удаляем старое
                await send_message_by_config(callback.message, msg_config, edit=False)
                await callback.message.delete()
            else:
                await state.clear()

                if score <= 3:
                    result_key = "wisdom_teeth_result_low"
                elif score <= 6:
                    result_key = "wisdom_teeth_result_medium"
                else:
                    result_key = "wisdom_teeth_result_high"

                result_config = WISDOM_MESSAGES[result_key]
                await send_message_by_config(callback.message, result_config, edit=False)

                async with AsyncSessionLocal() as session:
                    event_repo = EventRepository(session)
                    await event_repo.add_event(
                        user_id=callback.from_user.id,
                        event_name="wisdom_test_completed",
                        event_data={"score": score, "answers": answers, "result": result_key}
                    )

    elif callback_data == "start_main":
        await state.clear()
        from ..keyboards.main_menu import get_main_menu_keyboard
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

    elif callback_data == "consultation":
        from ..keyboards.contact import get_phone_keyboard
        await state.set_state(UserStates.consultation)
        await callback.message.delete()
        await callback.message.answer(
            "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
            reply_markup=get_phone_keyboard()
        )

    await callback.answer()


@router.callback_query(UserStates.bite_braces_test)
async def handle_bite_braces_test(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает ответы в тесте на брекеты"""
    callback_data = callback.data
    print(f"DEBUG: handle_bite_braces_test получил callback: {callback_data}") 

    data = await state.get_data()
    print(f"DEBUG: текущие данные state: {data}") 
    score = data.get("score", 0)
    answers = data.get("answers", {})

    if callback_data.startswith("bite_braces_q"):
        # Парсим callback_data: bite_braces_q{num}_{points}
        parts = callback_data.split("_")
        if len(parts) >= 4:
            question_part = parts[2]  # 'q1'
            question_num = int(question_part[1:])  # 1
            points = int(parts[3])  # 2, 1, 0

            answers[f"q{question_num}"] = points
            score += points
            await state.update_data(score=score, answers=answers)

            if question_num < 5:
                next_q = f"bite_braces_q{question_num + 1}"
                msg_config = BITE_MESSAGES[next_q]
                await send_message_by_config(callback.message, msg_config, edit=False)
                await callback.message.delete()
            else:
                await state.clear()

                # Определяем результат по сумме баллов
                if score <= 2:
                    result_key = "bite_result_no_braces"
                elif score <= 5:
                    result_key = "bite_result_consult"
                else:
                    result_key = "bite_result_need_braces"

                result_config = BITE_MESSAGES[result_key]
                await send_message_by_config(callback.message, result_config, edit=False)

                async with AsyncSessionLocal() as session:
                    event_repo = EventRepository(session)
                    await event_repo.add_event(
                        user_id=callback.from_user.id,
                        event_name="bite_braces_test_completed",
                        event_data={"score": score, "answers": answers, "result": result_key}
                    )

    elif callback_data == "start_main":
        await state.clear()
        from ..keyboards.main_menu import get_main_menu_keyboard
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

    elif callback_data == "consultation":
        from ..keyboards.contact import get_phone_keyboard
        await state.set_state(UserStates.consultation)
        await callback.message.delete()
        await callback.message.answer(
            "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
            reply_markup=get_phone_keyboard()
        )

    await callback.answer()


@router.callback_query(UserStates.wear_test)
async def handle_wear_test(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает ответы в тесте на стираемость (6 вопросов)"""
    callback_data = callback.data
    print(f"DEBUG: handle_wear_test получил callback: {callback_data}")  # для отладки

    data = await state.get_data()
    score = data.get("score", 0)
    answers = data.get("answers", {})

    if callback_data.startswith("wear_test_q"):
        # Парсим callback_data: wear_test_q{num}_{points}
        parts = callback_data.split("_")
        if len(parts) >= 4:
            question_part = parts[2]  # 'q1'
            question_num = int(question_part[1:])  # 1
            points = int(parts[3])  # 2, 1, 0

            answers[f"q{question_num}"] = points
            score += points
            await state.update_data(score=score, answers=answers)

            if question_num < 6:
                next_q = f"wear_test_q{question_num + 1}"
                msg_config = WEAR_MESSAGES[next_q]
                await send_message_by_config(callback.message, msg_config, edit=False)
                await callback.message.delete()
            else:
                await state.clear()

                # Определяем результат по сумме баллов (6 вопросов, максимум 12)
                if score <= 3:
                    result_key = "wear_result_low"
                elif score <= 7:
                    result_key = "wear_result_medium"
                elif score <= 10:
                    result_key = "wear_result_high"
                else:
                    result_key = "wear_result_critical"

                result_config = WEAR_MESSAGES[result_key]
                await send_message_by_config(callback.message, result_config, edit=False)

                async with AsyncSessionLocal() as session:
                    event_repo = EventRepository(session)
                    await event_repo.add_event(
                        user_id=callback.from_user.id,
                        event_name="wear_test_completed",
                        event_data={"score": score, "answers": answers, "result": result_key}
                    )

    elif callback_data == "start_main":
        await state.clear()
        from ..keyboards.main_menu import get_main_menu_keyboard
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )

    elif callback_data == "consultation":
        from ..keyboards.contact import get_phone_keyboard
        await state.set_state(UserStates.consultation)
        await callback.message.delete()
        await callback.message.answer(
            "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
            reply_markup=get_phone_keyboard()
        )

    await callback.answer()
