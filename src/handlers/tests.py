from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..db.session import AsyncSessionLocal
from ..repositories import EventRepository
from ..states.user_states import UserStates
from ..utils.message_sender import send_message_by_config
from ..messages.vncs import VNCS_MESSAGES

router = Router()


@router.callback_query(F.data == "start_test_vncs")
async def start_vncs_test(callback: CallbackQuery, state: FSMContext):
    """Начинает тест ВНЧС"""
    await state.set_state(UserStates.vncs_test)
    await state.update_data(score=0, answers={})

    msg_config = VNCS_MESSAGES["test_vncs_q1"]
    await send_message_by_config(callback.message, msg_config, edit=True)
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
