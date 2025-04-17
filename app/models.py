from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime

class DeviceStats(Base):
    __tablename__ = "device_stats"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    timestamp = Column(DateTime, default=lambda: datetime.utcnow().replace(second=0, microsecond=0))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    device_id = Column(String, ForeignKey("device_stats.device_id"), nullable=False)