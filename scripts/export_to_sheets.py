import asyncio
import json
import os
import sys

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import select

from src.config import settings
from src.db.session import AsyncSessionLocal
from src.models import Contact, User
from src.repositories import ContactRepository, EventRepository
from src.utils.time_utils import format_datetime, utc_to_msk

# ID таблицы (скопируй из URL)
SPREADSHEET_ID = settings.GOOGLE_SHEETS_ID

# Константы для колонок (чтобы не ошибиться)
COL_ID = 0
COL_DATE = 1
COL_FIRST_NAME = 2
COL_LAST_NAME = 3
COL_USERNAME = 4
COL_SOURCE = 5
COL_TEST = 6
COL_PHONE = 7
COL_RESULT = 8
COL_STATUS = 9


HEADERS = [
    "ID", "Дата", "Имя", "Фамилия", "Username",
    "Источник", "Тест", "Телефон", "Результат", "Статус"
]


def get_sheet():
    """Подключается к Google Sheets и возвращает рабочий лист"""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(
        "data/service_account.json",
        scopes=scopes
    )
    client = gspread.authorize(creds)
    return client.open_by_key(SPREADSHEET_ID).sheet1


def ensure_headers(sheet):
    """Проверяет наличие заголовков, добавляет если нет"""
    all_rows = sheet.get_all_values()
    if not all_rows or all_rows[0] != HEADERS:
        # Если таблица пустая или заголовки не совпадают
        sheet.clear()
        sheet.append_row(HEADERS)
        return True  # заголовки добавлены
    return False  # заголовки уже есть


async def get_contacts_with_events():
    """Собирает данные: контакты + последние тесты"""

    async with AsyncSessionLocal() as session:
        query = (
            select(Contact, User)
            .join(User, Contact.user_id == User.tg_id)
            .order_by(Contact.collected_at.desc())
        )
        result = await session.execute(query)
        rows = result.all()

        data = []
        for contact, user in rows:
            event_repo = EventRepository(session)
            last_test = await event_repo.get_last_test(contact.user_id)

            data.append({
                "contact": contact,
                "user": user,
                "last_test": last_test
            })

        return data


def export_to_sheets():
    """Основная функция выгрузки"""

    print("Сбор данных...")
    data = asyncio.run(get_contacts_with_events())

    print("Подключение к Google Sheets...")
    sheet = get_sheet()

    # Убеждаемся, что заголовки есть
    headers_added = ensure_headers(sheet)

    # Получаем все существующие ID
    existing_ids = set()
    all_rows = sheet.get_all_values()

    if len(all_rows) > 1:  # есть данные
        for row in all_rows[1:]:  # пропускаем заголовок
            if len(row) > COL_ID and row[COL_ID] and row[COL_ID].isdigit():
                existing_ids.add(int(row[COL_ID]))

    # Подготавливаем новые строки
    new_rows = []
    for item in data:
        contact = item["contact"]
        if contact.id not in existing_ids:
            user = item["user"]
            last_test = item["last_test"]

            row = [
                str(contact.id),
                format_datetime(utc_to_msk(contact.collected_at)),
                user.first_name or "",
                user.last_name or "",
                user.username or "",
                contact.source_step or "",
                last_test.get("test_name") if last_test else "",
                contact.phone,
                (last_test.get("result")[:300] if last_test else ""),
                "новый"
            ]
            new_rows.append(row)

    if new_rows:
        sheet.append_rows(new_rows)
        print(f"Добавлено {len(new_rows)} новых записей")
    else:
        print("Новых записей нет")


if __name__ == "__main__":
    export_to_sheets()
