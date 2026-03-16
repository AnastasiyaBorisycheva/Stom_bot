from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """Базовый класс для всех репозиториев"""

    def __init__(self, session: AsyncSession):
        self.session = session
