from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from models import User
from .base import BaseRepository


class UserRepository(BaseRepository):
    """Работа с пользователями в БД"""

    async def get_or_create(self, tg_id: int, username: str = None,
                            first_name: str = None, last_name: str = None,
                            source: str = None) -> User:
        """
        Получить пользователя по tg_id или создать нового.
        Возвращает пользователя и флаг "создан ли только что".
        """
        # Пытаемся найти существующего
        query = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        
        if user:
            # Обновляем last_seen
            user.last_seen = datetime.now()
            await self.session.commit()
            return user, False
        else:
            # Создаём нового
            user = User(
                tg_id=tg_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                source=source,
                first_seen=datetime.now(),
                last_seen=datetime.now()
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user, True

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        """Найти пользователя по tg_id"""
        query = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_last_seen(self, tg_id: int) -> None:
        """Обновить время последнего визита"""
        query = update(User).where(User.tg_id == tg_id).values(
            last_seen=datetime.now()
        )
        await self.session.execute(query)
        await self.session.commit()

    async def set_source(self, tg_id: int, source: str) -> None:
        """Установить источник (метку) для пользователя"""
        query = update(User).where(User.tg_id == tg_id).values(source=source)
        await self.session.execute(query)
        await self.session.commit()
