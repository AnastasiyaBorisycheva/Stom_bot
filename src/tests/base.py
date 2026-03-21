from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseTest(ABC):
    """Базовый класс для всех тестов"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Название теста"""
        pass

    @property
    @abstractmethod
    def start_state(self) -> str:
        """Имя состояния в FSM"""
        pass

    @property
    @abstractmethod
    def questions(self) -> List[Dict[str, Any]]:
        """Список вопросов"""
        pass

    @abstractmethod
    def get_result(self, answers: Dict[int, str]) -> str:
        """Результат теста"""
        pass
