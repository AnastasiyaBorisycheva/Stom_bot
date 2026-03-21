import json
from sqlalchemy.ext.asyncio import AsyncSession
from models import Event
from .base import BaseRepository
from utils.time_utils import now_utc


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
