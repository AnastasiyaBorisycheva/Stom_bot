from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from db.session import Base


class Contact(Base):
    __tablename__ = "contacts"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.tg_id"), nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    collected_at = Column(DateTime(timezone=True), nullable=False)
    source_step = Column(String, nullable=True)  # на каком шаге собрали
