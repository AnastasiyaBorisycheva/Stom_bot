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
        "Главное меню:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "consultation")
async def start_consultation(callback: CallbackQuery, state: FSMContext):
    """Начинает процесс записи на консультацию"""
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
    callback_data = callback.data
    print(f"[DEBUG] Получен callback_data: {callback_data}")
    
    # Получаем текущие данные
    data = await state.get_data()
    print(f"[DEBUG] Текущие данные state: {data}")
    score = data.get("score", 0)
    answers = data.get("answers", {})
    
    # Разбираем callback_data: test_vncs_q{num}_{points}
    # Пример: test_vncs_q1_2, test_vncs_q2_1, test_vncs_q3_0
    if callback_data.startswith("test_vncs_q"):
        parts = callback_data.split("_")
        print(f"[DEBUG] Разобранный parts: {parts}")
        # parts = ['test', 'vncs', 'q1', '2'] или ['test', 'vncs', 'q2', '1']
        if len(parts) >= 4:
            question_part = parts[2]  # 'q1'
            question_num = int(question_part[1:])  # 1, 2, 3...
            points = int(parts[3])  # 2, 1, 0

            print(f"[DEBUG] Вопрос {question_num}, баллы: {points}")
            
            # Сохраняем ответ
            answers[f"q{question_num}"] = points
            score += points
            await state.update_data(score=score, answers=answers)
            print(f"[DEBUG] Текущий счёт: {score}")
            
            # Определяем следующий вопрос
            if question_num < 5:
                next_q = f"test_vncs_q{question_num + 1}"
                print(f"[DEBUG] Следующий вопрос: {next_q}")
                msg_config = VNCS_MESSAGES[next_q]
                await send_message_by_config(callback.message, msg_config, edit=True)
            else:
                print(f"[DEBUG] Тест окончен, финальный счёт: {score}")
                # Тест окончен
                await state.clear()
                
                # Определяем результат по сумме баллов
                if score <= 2:
                    result_key = "result_vncs_normal"
                elif score <= 5:
                    result_key = "result_vncs_overload"
                elif score <= 7:
                    result_key = "result_vncs_dysfunction"
                else:
                    result_key = "result_vncs_pathology"

                print(f"[DEBUG] Результат: {result_key}")
                
                result_config = VNCS_MESSAGES[result_key]
                await send_message_by_config(callback.message, result_config, edit=True)
                
                # Сохраняем в events
                async with AsyncSessionLocal() as session:
                    event_repo = EventRepository(session)
                    await event_repo.add_event(
                        user_id=callback.from_user.id,
                        event_name="vncs_test_completed",
                        event_data={"score": score, "answers": answers, "result": result_key}
                    )
        else:
            print(f"[DEBUG] Неправильный формат callback_data: {callback_data}")

    elif callback_data == "start_main":
        # Возврат в главное меню
        print("[DEBUG] Возврат в главное меню")
        await state.clear()
        from ..keyboards.main_menu import get_main_menu_keyboard
        await callback.message.delete()
        await callback.message.answer(
            "Главное меню:",
            reply_markup=get_main_menu_keyboard()
        )
    
    elif callback_data == "consultation":
        # Запись на консультацию
        print("[DEBUG] Возврат в главное меню")
        from ..keyboards.contact import get_phone_keyboard
        await state.set_state(UserStates.consultation)
        await callback.message.delete()
        await callback.message.answer(
            "Для записи на приём нам нужен ваш номер телефона. Нажмите кнопку ниже:",
            reply_markup=get_phone_keyboard()
        )
    else:
        print(f"[DEBUG] Неизвестный callback_data: {callback_data}")
    
    await callback.answer()

