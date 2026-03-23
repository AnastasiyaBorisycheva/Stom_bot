# src/db/session.py

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base

from ..config import settings

DATABASE_URL = settings.DATABASE_URL

# Создаём движок (engine) — он отвечает за подключение к БД
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Показывает все SQL-запросы в консоли (помогает отлаживать)
)

# Создаём фабрику сессий
# Сессия — это "рабочее пространство" для общения с БД
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Базовый класс для моделей
Base = declarative_base()


async def init_db():
    """Создаёт таблицы в БД (если их нет)"""
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # если хочешь удалить всё и создать заново
        await conn.run_sync(Base.metadata.create_all)

    print("База данных готова (таблицы созданы)")
