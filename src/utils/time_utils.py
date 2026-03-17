from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pytz


# Часовой пояс Москвы
MSK_TZ = ZoneInfo("Europe/Moscow")


def now_utc() -> datetime:
    """Текущее время в UTC (для хранения в БД)"""
    return datetime.now(timezone.utc)


def utc_to_msk(utc_dt: datetime) -> datetime:
    """Конвертирует UTC в московское время"""
    if utc_dt.tzinfo is None:
        # Если время "наивное" (без зоны), считаем что это UTC
        utc_dt = utc_dt.replace(tzinfo=timezone.utc)
    return utc_dt.astimezone(MSK_TZ)


def now_msk() -> datetime:
    """Текущее московское время (для вывода)"""
    return datetime.now(MSK_TZ)


def format_msk(dt: datetime, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Форматирует время в московском поясе для вывода"""
    msk_dt = utc_to_msk(dt)
    return msk_dt.strftime(format)


def format_for_user(dt: datetime,
                    with_time: bool = True,
                    date_format: str = "%d.%m.%Y",
                    time_format: str = "%H:%M") -> str:
    """
    Форматирует дату для показа пользователю.

    Примеры:
    - только дата: 17.03.2026
    - дата и время: 17.03.2026 15:30
    """
    # Конвертируем в московское время
    msk_dt = utc_to_msk(dt)

    if with_time:
        return msk_dt.strftime(f"{date_format} {time_format}")
    else:
        return msk_dt.strftime(date_format)


# Удобные обёртки
def format_date(dt: datetime) -> str:
    """Только дата: 17.03.2026"""
    return format_for_user(dt, with_time=False)


def format_datetime(dt: datetime) -> str:
    """Дата и время: 17.03.2026 15:30"""
    return format_for_user(dt, with_time=True)


def format_for_excel(dt: datetime) -> str:
    """
    Формат для Excel (чтобы распознавался как дата)
    Можно использовать тот же, но Excel часто понимает ISO
    """
    # Для Excel лучше отдавать в ISO, он сам преобразует
    return dt.astimezone(MSK_TZ).isoformat(sep=' ', timespec='minutes')
