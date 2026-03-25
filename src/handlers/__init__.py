from .educational import router as educational_router
from .menu import router as menu_router
from .start import router as start_router
from .tests import router as tests_router

# Собираем все роутеры в список (удобно для подключения)
routers = [start_router, menu_router, educational_router, tests_router]

# Можно также экспортировать каждый отдельно
__all__ = ["start_router", "menu_router", "routers", "educational_router", "tests_router"]
