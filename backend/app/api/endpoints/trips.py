from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models import Trip, Itinerary, Expense, Destination, User
from backend.app.schemas import TripCreate, TripResponse, DayItinerary
from backend.app.api.deps import get_current_user

router = APIRouter(prefix="/trips", tags=["Trips Management"])


@router.get("", response_model=List[TripResponse])
def get_user_trips(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Trip).filter(Trip.user_id == current_user.id)
    if status and status != "All":
        query = query.filter(Trip.status == status)

    trips = query.order_by(Trip.created_at.desc()).all()
    results = []

    for t in trips:
        dest_name = t.destination.name if t.destination else t.title
        dest_state = t.destination.state if t.destination else ""
        dest_img = t.destination.image_url if t.destination else "https://images.unsplash.com/photo-1506461883276-594a12b11cf3?auto=format&fit=crop&w=800&q=80"
        
        days_parsed = []
        for itin in t.itineraries:
            days_parsed.append(DayItinerary(
                day_number=itin.day_number,
                date=itin.date,
                title=f"Day {itin.day_number}",
                activities=itin.activities_json,
                estimated_daily_expense=itin.estimated_daily_expense,
                transport_tips=itin.notes or ""
            ))

        expenses_parsed = [
            {
                "category": e.category,
                "estimated_amount": e.estimated_amount,
                "currency": e.currency
            }
            for e in t.expenses
        ]

        results.append(TripResponse(
            id=t.id,
            user_id=t.user_id,
            destination_id=t.destination_id,
            destination_name=dest_name,
            destination_state=dest_state,
            destination_image=dest_img,
            title=t.title,
            origin=t.origin,
            start_date=t.start_date,
            end_date=t.end_date,
            total_days=t.total_days,
            travellers_count=t.travellers_count,
            transport_mode=t.transport_mode,
            accommodation_type=t.accommodation_type,
            food_preference=t.food_preference,
            total_budget=t.total_budget,
            status=t.status,
            days=days_parsed,
            expenses=expenses_parsed
        ))

    return results


@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_in: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Lookup destination if name given
    dest = None
    if trip_in.destination_name:
        dest = db.query(Destination).filter(Destination.name.ilike(trip_in.destination_name)).first()

    new_trip = Trip(
        user_id=current_user.id,
        destination_id=dest.id if dest else trip_in.destination_id,
        title=trip_in.title or f"Trip to {trip_in.destination_name}",
        origin=trip_in.origin,
        start_date=trip_in.start_date,
        end_date=trip_in.end_date,
        total_days=trip_in.total_days,
        travellers_count=trip_in.travellers_count,
        transport_mode=trip_in.transport_mode,
        accommodation_type=trip_in.accommodation_type,
        food_preference=trip_in.food_preference,
        total_budget=trip_in.total_budget,
        status=trip_in.status or "Upcoming"
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    # Add itineraries if provided
    days_parsed = []
    if trip_in.days_data:
        for day in trip_in.days_data:
            act_dicts = [a.dict() if hasattr(a, "dict") else a for a in day.activities]
            itin = Itinerary(
                trip_id=new_trip.id,
                day_number=day.day_number,
                date=day.date,
                activities_json=act_dicts,
                estimated_daily_expense=day.estimated_daily_expense,
                notes=day.transport_tips
            )
            db.add(itin)
            days_parsed.append(day)
        db.commit()

    # Add expenses if provided
    expenses_parsed = []
    if trip_in.expense_breakdown:
        breakdown = trip_in.expense_breakdown
        categories = [
            ("Transportation", breakdown.transportation),
            ("Accommodation", breakdown.accommodation),
            ("Food", breakdown.food),
            ("Sightseeing", breakdown.sightseeing),
            ("Miscellaneous", breakdown.miscellaneous)
        ]
        for cat, amt in categories:
            exp = Expense(
                trip_id=new_trip.id,
                category=cat,
                estimated_amount=amt,
                currency=breakdown.currency
            )
            db.add(exp)
            expenses_parsed.append({"category": cat, "estimated_amount": amt, "currency": breakdown.currency})
        db.commit()

    return TripResponse(
        id=new_trip.id,
        user_id=new_trip.user_id,
        destination_id=new_trip.destination_id,
        destination_name=dest.name if dest else trip_in.destination_name,
        destination_state=dest.state if dest else "",
        destination_image=dest.image_url if dest else None,
        title=new_trip.title,
        origin=new_trip.origin,
        start_date=new_trip.start_date,
        end_date=new_trip.end_date,
        total_days=new_trip.total_days,
        travellers_count=new_trip.travellers_count,
        transport_mode=new_trip.transport_mode,
        accommodation_type=new_trip.accommodation_type,
        food_preference=new_trip.food_preference,
        total_budget=new_trip.total_budget,
        status=new_trip.status,
        days=days_parsed,
        expenses=expenses_parsed
    )


@router.get("/{id}", response_model=TripResponse)
def get_trip_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Trip).filter(Trip.id == id, Trip.user_id == current_user.id).first()
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found or you do not have permission to access it."
        )

    dest_name = t.destination.name if t.destination else t.title
    dest_state = t.destination.state if t.destination else ""
    dest_img = t.destination.image_url if t.destination else None

    days_parsed = []
    for itin in t.itineraries:
        days_parsed.append(DayItinerary(
            day_number=itin.day_number,
            date=itin.date,
            title=f"Day {itin.day_number}",
            activities=itin.activities_json,
            estimated_daily_expense=itin.estimated_daily_expense,
            transport_tips=itin.notes or ""
        ))

    expenses_parsed = [
        {"category": e.category, "estimated_amount": e.estimated_amount, "currency": e.currency}
        for e in t.expenses
    ]

    return TripResponse(
        id=t.id,
        user_id=t.user_id,
        destination_id=t.destination_id,
        destination_name=dest_name,
        destination_state=dest_state,
        destination_image=dest_img,
        title=t.title,
        origin=t.origin,
        start_date=t.start_date,
        end_date=t.end_date,
        total_days=t.total_days,
        travellers_count=t.travellers_count,
        transport_mode=t.transport_mode,
        accommodation_type=t.accommodation_type,
        food_preference=t.food_preference,
        total_budget=t.total_budget,
        status=t.status,
        days=days_parsed,
        expenses=expenses_parsed
    )


@router.delete("/{id}")
def delete_trip(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    t = db.query(Trip).filter(Trip.id == id, Trip.user_id == current_user.id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found or unauthorized")
    
    db.delete(t)
    db.commit()
    return {"message": "Trip successfully deleted"}
