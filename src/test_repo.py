# test_repo.py

import asyncio
import sys
import os

# Добавляем путь к проекту (чтобы работали импорты src)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.db.session import AsyncSessionLocal, Base
from src.repositories import UserRepository
from src.models import User

from utils.time_utils import utc_to_msk, format_msk, format_datetime, format_date

# ОЧИЩАЕМ МЕТАДАННЫЕ (чтобы избежать конфликта)
Base.metadata.clear()

async def test_user_repo():
    """Тестируем репозиторий пользователя"""
    print("🔍 Тестируем UserRepository...")
    
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        
        # 1. Создаём нового пользователя
        print("\n1. Создаём нового пользователя...")
        tg_id = 123456789
        user, created = await repo.get_or_create(
            tg_id=tg_id,
            username="test_user",
            first_name="Тест",
            last_name="Тестовый",
            source="VK_TMJ"
        )
        
        print(f"   Создан: {created}")
        print(f"   User ID: {user.id}")
        print(f"   TG ID: {user.tg_id}")
        print(f"   Username: {user.username}")
        print(f"   Source: {user.source}")
        print(f"   First seen: {user.first_seen}")
        print(f"   Last seen: {user.last_seen}")
        
        # 2. Пробуем получить того же пользователя
        print("\n2. Получаем существующего пользователя...")
        user2, created2 = await repo.get_or_create(tg_id=tg_id)
        
        print(f"   Создан заново: {created2} (должно быть False)")
        print(f"   Тот же пользователь: {user2.id == user.id}")
        
        # 3. Проверяем обновление last_seen
        print("\n3. Обновляем last_seen...")
        old_last_seen = user2.last_seen
        await asyncio.sleep(1)  # ждём секунду, чтобы время изменилось
        await repo.update_last_seen(tg_id)
        
        # Получаем обновлённые данные
        user3 = await repo.get_by_tg_id(tg_id)
        print(f"   Было: {old_last_seen}")
        print(f"   Стало: {user3.last_seen}")
        print(f"   Обновилось: {user3.last_seen > old_last_seen}")
        
        # 4. Проверяем установку source
        print("\n4. Устанавливаем новый source...")
        await repo.set_source(tg_id, "INST_WEAR")
        user4 = await repo.get_by_tg_id(tg_id)
        print(f"   Новый source: {user4.source}")
        
        # 5. Проверяем поиск по tg_id
        print("\n5. Ищем по tg_id...")
        found = await repo.get_by_tg_id(tg_id)
        print(f"   Найден: {found is not None}")
        print(f"   ID найденного: {found.id}")
        
        # 6. Пробуем найти несуществующего
        print("\n6. Ищем несуществующего пользователя...")
        not_found = await repo.get_by_tg_id(999999999)
        print(f"   Найден: {not_found is not None} (должно быть False)")

        print("\n7. Проверяем конвертацию времени:")
        user = await repo.get_by_tg_id(tg_id)
        print(f"   Время в БД (UTC): {user.last_seen}")
        print(f"   Время московское: {utc_to_msk(user.last_seen)}")
        print(f"   Отформатированное: {format_msk(user.last_seen)}")

        print("\n8. Проверяем форматирование для пользователей:")
        user = await repo.get_by_tg_id(tg_id)
        print(f"   Дата в БД (UTC): {user.last_seen}")
        print(f"   Для пользователя (дата): {format_date(user.last_seen)}")
        print(f"   Для пользователя (дата+время): {format_datetime(user.last_seen)}")
    
    print("\n✅ Тестирование завершено!")

if __name__ == "__main__":
    asyncio.run(test_user_repo())
