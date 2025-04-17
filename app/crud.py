from sqlalchemy.orm import Session
from sqlalchemy import func
import statistics
from datetime import datetime
from typing import Optional, List, Tuple
from schemas import DeviceStatsCreate, DeviceStats, DeviceAnalytics, UserCreate, User
from models import DeviceStats as DeviceStatsModel, User as UserModel

def create_user(db: Session, user: UserCreate):
    device = db.query(DeviceStatsModel).filter(DeviceStatsModel.device_id == user.device_id).first()
    if not device:
        raise ValueError(f"Устройство с id {user.device_id} не найдено")
    
    db_user = UserModel(name=user.name, device_id=user.device_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_device_stats(db: Session, device_id: str, stats: DeviceStatsCreate):
    db_stats = DeviceStatsModel(device_id=device_id, **stats.dict())
    db.add(db_stats)
    db.commit()
    db.refresh(db_stats)
    return db_stats

def get_device_analytics(db: Session, device_id: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    query = db.query(DeviceStatsModel).filter(DeviceStatsModel.device_id == device_id)
    if start_time:
        query = query.filter(DeviceStatsModel.timestamp >= start_time)
    if end_time:
        query = query.filter(DeviceStatsModel.timestamp <= end_time)
    
    stats = query.all()
    if not stats:
        return None
    
    count = len(stats)
    x_values = [stat.x for stat in stats]
    y_values = [stat.y for stat in stats]
    z_values = [stat.z for stat in stats]
    
    return DeviceAnalytics(
        device_id=device_id,
        user_id=None,
        min_x=min(x_values),
        max_x=max(x_values),
        count=count,
        sum_x=sum(x_values),
        median_x=statistics.median(x_values) if x_values else 0.0,
        min_y=min(y_values),
        max_y=max(y_values),
        sum_y=sum(y_values),
        median_y=statistics.median(y_values) if y_values else 0.0,
        min_z=min(z_values),
        max_z=max(z_values),
        sum_z=sum(z_values),
        median_z=statistics.median(z_values) if z_values else 0.0
    )

def get_user_analytics(db: Session, user_id: int, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None):
    user = get_user(db, user_id)
    if not user:
        return None
    
    query = db.query(DeviceStatsModel).filter(DeviceStatsModel.device_id == user.device_id)
    if start_time:
        query = query.filter(DeviceStatsModel.timestamp >= start_time)
    if end_time:
        query = query.filter(DeviceStatsModel.timestamp <= end_time)
    
    stats = query.all()
    if not stats:
        return None
    
    count = len(stats)
    x_values = [stat.x for stat in stats]
    y_values = [stat.y for stat in stats]
    z_values = [stat.z for stat in stats]
    
    return DeviceAnalytics(
        device_id=user.device_id,
        user_id=user_id,
        min_x=min(x_values) if x_values else 0.0,
        max_x=max(x_values) if x_values else 0.0,
        count=count,
        sum_x=sum(x_values) if x_values else 0.0,
        median_x=statistics.median(x_values) if x_values else 0.0,
        min_y=min(y_values) if y_values else 0.0,
        max_y=max(y_values) if y_values else 0.0,
        sum_y=sum(y_values) if y_values else 0.0,
        median_y=statistics.median(y_values) if y_values else 0.0,
        min_z=min(z_values) if z_values else 0.0,
        max_z=max(z_values) if z_values else 0.0,
        sum_z=sum(z_values) if z_values else 0.0,
        median_z=statistics.median(z_values) if z_values else 0.0
    )

def get_user_devices(db: Session, user_id: int) -> List[Tuple[str, str]]:
    user = get_user(db, user_id)
    if not user:
        return []
    return [(user.device_id, user.device_id)]