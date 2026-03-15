# init_db.py (временный, потом удалим)

import asyncio
from db.session import init_db, engine
from models.base_model import TestUser  # чтобы модель "подцепилась"


async def main():
    print("Создаю базу данных...")
    await init_db()
    print("Готово!")
    
    # Закрываем соединения
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())
