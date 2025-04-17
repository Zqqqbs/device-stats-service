from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from schemas import DeviceStats, DeviceStatsCreate, DeviceAnalytics, User, UserCreate
from crud import create_device_stats, get_device_analytics, create_user, get_user, get_user_analytics, get_user_devices
from tasks import analyze_device_stats
from database import Base, engine, get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url="/docs", redoc_url="/redoc", debug=True)

@app.post("/devices/{device_id}/stats", response_model=DeviceStats)
async def add_stats(device_id: str, stats: DeviceStatsCreate, db: Session = Depends(get_db)):
    try:
        db_stats = create_device_stats(db, device_id, stats)
        analyze_device_stats.delay(device_id)
        return db_stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошмбка добавления данных: {str(e)}")

@app.get("/devices/{device_id}/stats", response_model=DeviceStats)
async def get_latest_stats(device_id: str, db: Session = Depends(get_db)):
    stats = db.query(models.DeviceStats).filter(models.DeviceStats.device_id == device_id).order_by(models.DeviceStats.timestamp.desc()).first()
    if not stats:
        raise HTTPException(status_code=404, detail="Не найдено информации по этому устройству")
    return stats

@app.get("/devices/{device_id}/analytics", response_model=DeviceAnalytics)
async def get_device_analytics_endpoint(device_id: str, db: Session = Depends(get_db)):
    analytics = get_device_analytics(db, device_id, None, None)
    if not analytics:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return analytics

@app.get("/devices/{device_id}/analytics/period", response_model=DeviceAnalytics)
async def get_device_analytics_period(
    device_id: str,
    start_time: str = Query(..., description="Дата начала в формате ГГГГ-ММ-ДД ЧЧ:ММ (например - 2025-04-16 17:19)"),
    end_time: str = Query(..., description="Дата конца в формате ГГГГ-ММ-ДД ЧЧ:ММ (например - 2025-04-16 17:19)"),
    db: Session = Depends(get_db)
):
    try:
        start = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        end = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        if start > end:
            raise ValueError("Дата начала должна быть раньше даты конца")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Неверный формат даты: {str(e)}. Используйте формат ГГГГ-ММ-ДД ЧЧ:ММ (например - 2025-04-16 17:19)")

    analytics = get_device_analytics(db, device_id, start, end)
    if not analytics:
        raise HTTPException(status_code=404, detail="Не найдено данных по заданному периоду")
    return analytics

@app.post("/users/", response_model=User)
async def add_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@app.get("/users/{user_id}/analytics", response_model=DeviceAnalytics)
async def get_user_analytics_endpoint(user_id: int, db: Session = Depends(get_db)):
    analytics = get_user_analytics(db, user_id, None, None)
    if not analytics:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    return analytics

@app.get("/users/{user_id}/devices-analytics", response_model=List[DeviceAnalytics])
async def get_user_devices_analytics(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не нвйден")
    devices = get_user_devices(db, user_id)
    device_analytics = []
    for device in devices:
        device_id = device[0]
        device_analytic = get_device_analytics(db, device_id, None, None)
        if device_analytic:
            device_analytics.append(device_analytic)
    return device_analytics