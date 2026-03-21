from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    main_menu = State()
    test_active = State()   # ← общее состояние для всех тестов
