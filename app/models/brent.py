from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, Integer
from app.core.database import Base


class BrentValue(Base):
    __tablename__ = "brent_values"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))