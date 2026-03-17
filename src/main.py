# src/main.py

import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import settings  # у тебя есть файл с настройками?
from handlers import router  # импортируем наш роутер

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

# Подключаем роутер с хендлерами
dp.include_router(router)


async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
