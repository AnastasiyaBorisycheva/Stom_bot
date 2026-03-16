# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import asyncio
from db.session import init_db, engine
from models import User, State, Contact, Event

async def main():
    print("Создаю таблицы...")
    await init_db()
    print("Готово!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())