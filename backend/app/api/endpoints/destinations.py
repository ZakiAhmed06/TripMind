from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from backend.app.database.session import get_db
from backend.app.models import Destination, Attraction
from backend.app.schemas import DestinationResponse, DestinationDetailResponse

router = APIRouter(prefix="/destinations", tags=["Destinations"])


@router.get("", response_model=List[DestinationResponse])
def get_destinations(
    query: Optional[str] = Query(None, description="Search term for destination name or state"),
    category: Optional[str] = Query(None, description="Filter by category"),
    state: Optional[str] = Query(None, description="Filter by state"),
    max_budget: Optional[float] = Query(None, description="Maximum average daily budget"),
    season: Optional[str] = Query(None, description="Filter by best season keyword"),
    limit: int = Query(50, ge=1, le=400),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    q = db.query(Destination)

    if query:
        search_filter = or_(
            Destination.name.ilike(f"%{query}%"),
            Destination.state.ilike(f"%{query}%"),
            Destination.category.ilike(f"%{query}%"),
            Destination.description.ilike(f"%{query}%")
        )
        q = q.filter(search_filter)

    if category and category != "All":
        q = q.filter(Destination.category.ilike(f"%{category}%"))

    if state and state != "All":
        q = q.filter(Destination.state.ilike(f"%{state}%"))

    if max_budget:
        q = q.filter(Destination.average_budget <= max_budget)

    if season and season != "All":
        q = q.filter(Destination.best_season.ilike(f"%{season}%"))

    # Order by popularity score descending
    destinations = q.order_by(Destination.popularity_score.desc()).offset(offset).limit(limit).all()
    return destinations


@router.get("/search", response_model=List[DestinationResponse])
def search_destinations(
    q: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    results = db.query(Destination).filter(
        or_(
            Destination.name.ilike(f"%{q}%"),
            Destination.state.ilike(f"%{q}%")
        )
    ).limit(limit).all()
    return results


@router.get("/{id}", response_model=DestinationDetailResponse)
def get_destination_details(id: int, db: Session = Depends(get_db)):
    destination = db.query(Destination).filter(Destination.id == id).first()
    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Destination with ID {id} not found."
        )

    # Attach attractions ordered by popularity rank
    attractions = db.query(Attraction).filter(Attraction.destination_id == id).order_by(Attraction.popularity_rank.asc()).all()
    
    resp_dict = {
        "id": destination.id,
        "name": destination.name,
        "state": destination.state,
        "country": destination.country,
        "category": destination.category,
        "average_budget": destination.average_budget,
        "average_temperature": destination.average_temperature,
        "adventure_score": destination.adventure_score,
        "nature_score": destination.nature_score,
        "nightlife_score": destination.nightlife_score,
        "heritage_score": destination.heritage_score,
        "photography_score": destination.photography_score,
        "family_friendly": destination.family_friendly,
        "best_season": destination.best_season,
        "popularity_score": destination.popularity_score,
        "latitude": destination.latitude,
        "longitude": destination.longitude,
        "description": destination.description,
        "image_url": destination.image_url,
        "attractions": attractions
    }
    return resp_dict
