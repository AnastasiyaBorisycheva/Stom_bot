from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Contact
from src.utils.time_utils import now_utc

from .base import BaseRepository


class ContactRepository(BaseRepository):

    async def save_contact(
        self,
        user_id: int,
        phone: str,
        email: str = None,
        source_step: str = None
    ) -> Contact:
        """Сохраняет контакт пользователя"""

        contact = Contact(
            user_id=user_id,
            phone=phone,
            email=email,
            collected_at=now_utc(),
            source_step=source_step
        )
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return contact

    async def save_or_update_contact(
        self,
        user_id: int,
        phone: str,
        email: str = None,
        source_step: str = None
    ) -> Contact:
        """Сохраняет или обновляет контакт пользователя (не создаёт дубли)"""

        # Нормализуем номер: убираем всё кроме цифр
        normalized_phone = self._normalize_phone(phone)

        # Ищем существующий контакт
        query = select(Contact).where(Contact.user_id == user_id)
        result = await self.session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            # Обновляем существующий
            existing.phone = normalized_phone
            if email:
                existing.email = email
            if source_step:
                existing.source_step = source_step
            existing.collected_at = now_utc()  # обновляем время
            await self.session.commit()
            await self.session.refresh(existing)
            return existing
        else:
            # Создаём новый
            contact = Contact(
                user_id=user_id,
                phone=normalized_phone,
                email=email,
                collected_at=now_utc(),
                source_step=source_step
            )
            self.session.add(contact)
            await self.session.commit()
            await self.session.refresh(contact)
            return contact       

    def _normalize_phone(self, phone: str) -> str:
        """Приводит номер телефона к единому формату (только цифры)"""
        # Убираем всё, кроме цифр
        digits = ''.join(filter(str.isdigit, phone))

        # Если номер начинается с 8 и имеет 11 цифр, заменяем на +7
        if len(digits) == 11 and digits.startswith('8'):
            digits = '7' + digits[1:]

        # Если номер начинается с 7 и имеет 11 цифр, оставляем как есть
        if len(digits) == 11 and digits.startswith('7'):
            return '+' + digits

        # Если номер другой длины, возвращаем как есть (с плюсом, если есть)
        # Но лучше всегда хранить в формате +7XXXXXXXXXX
        if phone.startswith('+'):
            return phone
        return '+' + digits if digits else phone

    async def get_contacts_by_user(self, user_id: int):
        """Получить все контакты пользователя"""
        query = select(Contact).where(Contact.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_contacts(self) -> list[Contact]:
        """Получить все контакты"""

        query = select(Contact)
        result = await self.session.execute(query)
        return result.scalars().all()
