from src.models.base import Base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

class Log(Base):
    __tablename__ = "logging"
    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20))
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
