from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceStatsBase(BaseModel):
    x: float
    y: float
    z: float

class DeviceStatsCreate(DeviceStatsBase):
    pass

class DeviceStats(DeviceStatsBase):
    id: int
    device_id: str
    timestamp: datetime

    class Config:
        orm_mode = True

class DeviceAnalytics(BaseModel):
    device_id: str
    user_id: Optional[int] = None
    min_x: float
    max_x: float
    count: int
    sum_x: float
    median_x: float
    min_y: float
    max_y: float
    sum_y: float
    median_y: float
    min_z: float
    max_z: float
    sum_z: float
    median_z: float

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    device_id: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True