from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.database.session import get_db
from backend.app.models import ChatSession, ChatMessage, User
from backend.app.schemas import ChatMessageRequest, ChatMessageResponse
from backend.app.genai.assistant_service import handle_assistant_chat
from backend.app.api.deps import get_current_user

router = APIRouter(prefix="/assistant", tags=["AI Travel Assistant"])


@router.post("/chat", response_model=ChatMessageResponse)
def chat_with_assistant(
    req: ChatMessageRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        response = handle_assistant_chat(req, db, user_id=current_user.id)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assistant service error: {str(e)}"
        )


@router.get("/history/{session_id}")
def get_chat_history(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chat session not found")

    messages = db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()
    
    return {
        "session_id": session.id,
        "title": session.session_title,
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in messages
        ]
    }
