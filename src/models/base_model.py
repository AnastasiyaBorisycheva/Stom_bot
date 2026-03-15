# src/models/base_model.py

from sqlalchemy import Column, Integer, String
from db.session import Base


class TestUser(Base):
    __tablename__ = "test_users"  # имя таблицы в БД

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
