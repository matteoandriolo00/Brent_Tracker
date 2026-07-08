from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from app.core.database import Base


class BrentValue(Base):
    __tablename__ = "brent_values"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.now(datetime.timezone.utc))