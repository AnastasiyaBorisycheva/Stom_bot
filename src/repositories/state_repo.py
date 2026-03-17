import json
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import State
from .base import BaseRepository
from utils.time_utils import now_utc


class StateRepository(BaseRepository):
    """Работа с состояниями пользователей"""

    async def get_state(self, user_id: int) -> tuple[str | None, dict]:
        """
        Получить текущее состояние пользователя.
        Возвращает (current_state, data)
        """
        query = select(State).where(State.user_id == user_id)
        result = await self.session.execute(query)
        state = result.scalar_one_or_none()

        if state:
            data = json.loads(state.data) if state.data else {}
            return state.current_state, data
        return None, {}

    async def set_state(
            self,
            user_id: int,
            state_name: str,
            data: dict = None
    ) -> None:

        """
        Установить состояние пользователя.
        Если запись есть — обновляет, если нет — создаёт.
        """
        # Проверяем, есть ли уже запись
        query = select(State).where(State.user_id == user_id)
        result = await self.session.execute(query)
        state = result.scalar_one_or_none()

        now = now_utc()
        
        if state:
            # Обновляем существующую
            state.current_state = state_name
            if data is not None:
                state.data = json.dumps(data, ensure_ascii=False)
            state.updated_at = now
        else:
            # Создаём новую
            new_state = State(
                user_id=user_id,
                current_state=state_name,
                data=json.dumps(data, ensure_ascii=False) if data else None,
                updated_at=now
            )
            self.session.add(new_state)

        await self.session.commit()

    async def update_data(self, user_id: int, data: dict) -> None:
        """
        Обновить только данные (не меняя состояние).
        Полезно для накопления ответов в тесте.
        """
        query = select(State).where(State.user_id == user_id)
        result = await self.session.execute(query)
        state = result.scalar_one_or_none()

        if state:
            current_data = json.loads(state.data) if state.data else {}
            current_data.update(data)
            state.data = json.dumps(current_data, ensure_ascii=False)
            state.updated_at = now_utc()
            await self.session.commit()

    async def clear_state(self, user_id: int) -> None:
        """Сбросить состояние пользователя (удалить запись)"""
        query = select(State).where(State.user_id == user_id)
        result = await self.session.execute(query)
        state = result.scalar_one_or_none()

        if state:
            await self.session.delete(state)
            await self.session.commit()
