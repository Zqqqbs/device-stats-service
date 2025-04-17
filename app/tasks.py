from celery import Celery
from database import SessionLocal
from crud import get_device_analytics

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def analyze_device_stats(device_id: str):
    db = SessionLocal()
    try:
        analytics = get_device_analytics(db, device_id, None, None)
        if not analytics:
            print(f"Нет данных по устройству {device_id}")
        else:
            print(f"Данные по устройству {device_id}: {analytics}")
    except Exception as e:
        print(f"Ошибка при попытке аналитики устройства: {str(e)}")
    finally:
        db.close()