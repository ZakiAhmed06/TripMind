from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models import Feedback, User, Destination
from backend.app.schemas import FeedbackCreate, FeedbackResponse
from backend.app.api.deps import get_current_user

router = APIRouter(prefix="/feedback", tags=["User Preference Feedback"])


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    fb_in: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    feedback = Feedback(
        user_id=current_user.id,
        destination_id=fb_in.destination_id,
        trip_id=fb_in.trip_id,
        rating=fb_in.rating,
        liked=fb_in.liked,
        review=fb_in.review
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/destination/{destination_id}", response_model=List[FeedbackResponse])
def get_destination_feedback(destination_id: int, db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).filter(Feedback.destination_id == destination_id).order_by(Feedback.created_at.desc()).limit(20).all()
    return feedbacks
