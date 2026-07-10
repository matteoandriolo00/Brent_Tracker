from sqlalchemy import Column, Float, Integer, String
from app.core.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    target_price = Column(Float, nullable=False)
    direction = Column(String, nullable=False)  # Valori attesi: "ABOVE" o "BELOW"
    status = Column(String, default="ACTIVE", index=True)  # Valori attesi: "ACTIVE" o "TRIGGERED"