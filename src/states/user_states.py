from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    main_menu = State()
    education = State()

    vncs_test = State()
    wisdom_test = State()
    bite_braces_test = State()
    wear_test = State()
    test_active = State()   # ← общее состояние для всех тестов

    consultation = State()
    phone_waiting = State()
