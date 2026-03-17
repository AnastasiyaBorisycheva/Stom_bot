# test_state_repo.py

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.db.session import AsyncSessionLocal
from src.repositories import StateRepository

async def test_state_repo():
    print("🔍 Тестируем StateRepository...")
    
    async with AsyncSessionLocal() as session:
        repo = StateRepository(session)
        user_id = 123456789  # тот же, что в тесте пользователя
        
        # 1. Устанавливаем состояние
        print("\n1. Устанавливаем состояние 'test_state' с данными...")
        await repo.set_state(user_id, "test_state", {"answer": 42, "step": 1})
        
        # 2. Получаем состояние
        print("\n2. Получаем состояние...")
        state, data = await repo.get_state(user_id)
        print(f"   State: {state}")
        print(f"   Data: {data}")
        
        # 3. Обновляем данные
        print("\n3. Обновляем данные...")
        await repo.update_data(user_id, {"answer": 43, "new_field": "hello"})
        state, data = await repo.get_state(user_id)
        print(f"   Новые данные: {data}")
        
        # 4. Меняем состояние
        print("\n4. Меняем состояние...")
        await repo.set_state(user_id, "new_state", {"finished": True})
        state, data = await repo.get_state(user_id)
        print(f"   Новое состояние: {state}")
        print(f"   Новые данные: {data}")
        
        # 5. Сбрасываем состояние
        print("\n5. Сбрасываем состояние...")
        await repo.clear_state(user_id)
        state, data = await repo.get_state(user_id)
        print(f"   После сброса: state={state}, data={data}")
    
    print("\n✅ Тест завершён!")

if __name__ == "__main__":
    asyncio.run(test_state_repo())