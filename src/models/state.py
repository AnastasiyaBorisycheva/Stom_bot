from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.session import Base


class State(Base):
    __tablename__ = "states"

    user_id = Column(Integer, ForeignKey("users.tg_id"), primary_key=True)
    current_state = Column(String, nullable=False)  # например, 'bite_test_q1'
    data = Column(String, nullable=True)  # JSON с доп. данными
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
