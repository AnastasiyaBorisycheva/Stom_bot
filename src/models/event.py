from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.session import Base


class Event(Base):
    __tablename__ = "events"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.tg_id"), nullable=False)
    event_name = Column(String, nullable=False)  # 'start', 'problem_selected'
    event_data = Column(String, nullable=True)  # JSON
    created_at = Column(DateTime(timezone=True), nullable=False)
