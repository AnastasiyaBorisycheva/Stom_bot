import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import settings
from .db.session import init_db
from .handlers import routers

# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def on_startup():
    """Действия при запуске бота"""
    print("Инициализация базы данных...")
    await init_db()
    print("База данных готова")


async def on_shutdown():
    """Действия при остановке бота"""
    print("Бот остановлен")


def create_bot_and_dispatcher() -> tuple[Bot, Dispatcher]:
    """Создаёт и настраивает бота и диспетчер"""
    bot = Bot(token=settings.BOT_TOKEN)
    storage = MemoryStorage()  # пока память, потом можно Redis
    dp = Dispatcher(storage=storage)

    # Подключаем роутеры
    dp.include_routers(*routers)

    # Регистрируем хуки (можно и в main, но так чище)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    return bot, dp


async def main():
    bot, dp = create_bot_and_dispatcher()

    print("Бот запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
