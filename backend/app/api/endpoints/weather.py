from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models import Destination
from backend.app.services.weather_service import get_weather_forecast

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/{destination_id}")
def get_weather(destination_id: int, db: Session = Depends(get_db)):
    dest = db.query(Destination).filter(Destination.id == destination_id).first()
    if not dest:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Destination not found")

    forecast = get_weather_forecast(
        lat=dest.latitude,
        lon=dest.longitude,
        destination_id=dest.id,
        db=db
    )
    forecast["destination_name"] = dest.name
    return forecast
