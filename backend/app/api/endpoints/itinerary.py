from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models import Itinerary, Trip, Destination
from backend.app.schemas import (
    ItineraryGenerateRequest,
    ItineraryResponse,
    ItineraryUpdateRequest,
    ReplanningRequest,
    DayItinerary
)
from backend.app.genai.gemini_service import generate_structured_itinerary
from backend.app.genai.replanning_service import replan_day_itinerary
from backend.app.api.deps import get_optional_current_user

router = APIRouter(prefix="/itinerary", tags=["Itinerary Generation & Replanning"])


@router.post("/generate", response_model=ItineraryResponse)
def generate_itinerary(req: ItineraryGenerateRequest):
    try:
        response = generate_structured_itinerary(req)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate itinerary: {str(e)}"
        )


@router.post("/replan", response_model=List[DayItinerary])
def replan_itinerary(req: ReplanningRequest):
    try:
        revised_days = replan_day_itinerary(req)
        return revised_days
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Replanning error: {str(e)}"
        )


@router.get("/{id}", response_model=DayItinerary)
def get_itinerary_day(id: int, db: Session = Depends(get_db)):
    itin = db.query(Itinerary).filter(Itinerary.id == id).first()
    if not itin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary day not found")
    
    return DayItinerary(
        day_number=itin.day_number,
        date=itin.date,
        title=f"Day {itin.day_number}",
        activities=itin.activities_json,
        estimated_daily_expense=itin.estimated_daily_expense,
        notes=itin.notes
    )


@router.put("/{id}")
def update_itinerary_day(id: int, req: DayItinerary, db: Session = Depends(get_db)):
    itin = db.query(Itinerary).filter(Itinerary.id == id).first()
    if not itin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary day not found")

    itin.activities_json = [a.dict() if hasattr(a, "dict") else a for a in req.activities]
    itin.estimated_daily_expense = req.estimated_daily_expense
    itin.notes = req.transport_tips
    db.commit()
    return {"message": "Itinerary day updated successfully"}


@router.delete("/{id}")
def delete_itinerary_day(id: int, db: Session = Depends(get_db)):
    itin = db.query(Itinerary).filter(Itinerary.id == id).first()
    if not itin:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Itinerary day not found")
    db.delete(itin)
    db.commit()
    return {"message": "Itinerary day removed successfully"}
