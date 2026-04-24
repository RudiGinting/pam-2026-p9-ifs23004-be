from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.extensions import Base

class RequestLog(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True)
    disease = Column(String(200))
    total = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))