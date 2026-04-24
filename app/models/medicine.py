from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from app.extensions import Base

class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(Text)
    indication = Column(Text)
    dosage = Column(Text)
    side_effect = Column(Text)
    request_id = Column(Integer, ForeignKey("requests.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))