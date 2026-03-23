import json
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Event
from .base import BaseRepository
from src.utils.time_utils import now_utc
from sqlalchemy import select, desc


class EventRepository(BaseRepository):

    async def add_event(
        self,
        user_id: int,
        event_name: str,
        event_data: dict = None
    ) -> Event:
        """Сохраняет событие"""

        event = Event(
            user_id=user_id,
            event_name=event_name,
            event_data=json.dumps(event_data, ensure_ascii=False) if event_data else None,
            created_at=now_utc()
        )
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event

    async def get_last_test(self, user_id: int) -> dict | None:
        """Получить последний тест пользователя"""

        query = (
            select(Event)
            .where(Event.user_id == user_id)
            .where(Event.event_name.like("test_completed_%"))
            .order_by(desc(Event.created_at))
            .limit(1)
        )
        result = await self.session.execute(query)
        event = result.scalar_one_or_none()

        if event:
            return {
                "test_name": event.event_name.replace("test_completed_", ""),
                "answers": json.loads(event.event_data) if event.event_data else {},
                "result": json.loads(event.event_data).get("result", "") if event.event_data else "",
                "created_at": event.created_at
            }
        return None
