"""
Contextual Conversational AI Travel Assistant Service
Maintains trip context, queries FAISS RAG knowledge base, and interacts via Gemini / fallback generator.
"""
import os
import json
import logging
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.models import ChatSession, ChatMessage
from backend.app.schemas import ChatMessageRequest, ChatMessageResponse
from backend.app.genai.rag_service import retrieve_context

logger = logging.getLogger(__name__)


def handle_assistant_chat(req: ChatMessageRequest, db: Session, user_id: int) -> ChatMessageResponse:
    # 1. Retrieve or create chat session
    session = None
    if req.session_id:
        session = db.query(ChatSession).filter(ChatSession.id == req.session_id, ChatSession.user_id == user_id).first()
    
    if not session:
        session_title = f"{req.current_destination or 'Travel'} Planning Assistant"
        session = ChatSession(
            user_id=user_id,
            trip_id=req.trip_id,
            session_title=session_title
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    # 2. Save user message to database
    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=req.message,
        metadata_json={
            "destination": req.current_destination,
            "budget": req.current_budget
        }
    )
    db.add(user_msg)
    db.commit()

    # 3. Retrieve past conversation history (last 6 messages)
    history = db.query(ChatMessage).filter(ChatMessage.session_id == session.id).order_by(ChatMessage.id.desc()).limit(6).all()
    history = list(reversed(history))

    # 4. RAG Retrieval from knowledge base
    query_text = f"{req.current_destination or ''} {req.message}".strip()
    rag_chunks = retrieve_context(query_text, top_k=2)
    sources = [f"{c['destination']} ({c['section']})" for c in rag_chunks]
    context_text = "\n\n".join([c["content"] for c in rag_chunks]) if rag_chunks else "No specific documents found."

    # 5. Generate AI reply
    assistant_reply = None
    suggested_actions = []

    # Check for Gemini Client
    if settings.GEMINI_API_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            prompt = f"""You are TripMind AI Assistant, a courteous, highly knowledgeable personal travel planning concierge.
Current Trip Destination: {req.current_destination or 'Not specified'}
Current Budget: INR {req.current_budget or 'Not specified'}

VERIFIED RAG KNOWLEDGE BASE:
{context_text}

USER MESSAGE: {req.message}

INSTRUCTIONS:
1. Provide a direct, helpful, grounded answer based on the knowledge base when available.
2. If the user asks about budget reduction, give concrete tips (e.g. opting for 3-star standard homestays, sleeper/3AC trains, self-guided audio walks).
3. Be concise and friendly."""

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt
            )
            assistant_reply = response.text.strip()
        except Exception as e:
            logger.warning("Gemini Assistant call failed (%s), using intelligent rule-based concierge fallback.", e)

    # Fallback contextual replies if Gemini key is not supplied or fails
    if not assistant_reply:
        msg_l = req.message.lower()
        dest = req.current_destination or "your selected destination"
        
        if "budget" in msg_l or "cheaper" in msg_l or "reduce" in msg_l:
            assistant_reply = (
                f"To optimize your budget in {dest}, I recommend:\n"
                f"1. **Accommodation:** Switch to government tourism guest houses or verified homestays (saves ~₹1,200/night).\n"
                f"2. **Transit:** Use shared cabs or local state transport buses between major attractions.\n"
                f"3. **Food:** Enjoy authentic local thali restaurants and street food hubs rather than resort cafes.\n"
                f"Would you like me to recalculate your estimated expenses?"
            )
            suggested_actions = ["Recalculate with Budget Hotel", "Switch to Train Transit", "View Expense Breakdown"]
        elif "monsoon" in msg_l or "rain" in msg_l or "weather" in msg_l:
            assistant_reply = (
                f"During monsoon in {dest}, outdoor treks or high-altitude passes may experience heavy precipitation or roadblocks. "
                f"I recommend planning indoor cultural visits, monasteries, museums, and cozy tea lounge experiences. "
                f"You can use our **Simulate Weather Alert & Replan** button to automatically swap outdoor activities for rain-safe alternatives!"
            )
            suggested_actions = ["Simulate Weather Alert & Replan", "Check 7-Day Forecast", "View Indoor Attractions"]
        elif "family" in msg_l or "kid" in msg_l:
            assistant_reply = (
                f"For a family trip to {dest}, I suggest keeping travel paces relaxed with no more than 2-3 attractions daily, "
                f"choosing family-friendly resorts with dining options, and scheduling early-morning departures."
            )
            suggested_actions = ["Adjust Daily Pace", "Suggest Family Stays", "View Leisure Itinerary"]
        else:
            rag_snippet = ""
            if rag_chunks:
                rag_snippet = f"\n\n**From Verified Knowledge Base:**\n{rag_chunks[0]['content'][:300]}..."
            assistant_reply = (
                f"Here are key insights for {dest}:\n"
                f"The best season for travel is typically between October and May. "
                f"We recommend booking popular monument visits early morning to avoid peak hours."
                f"{rag_snippet}"
            )
            suggested_actions = ["Show Day 1 Schedule", "Reduce Budget", "Check Crowd Levels"]

    # 6. Save assistant message to database
    bot_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=assistant_reply,
        metadata_json={"sources": sources}
    )
    db.add(bot_msg)
    db.commit()

    return ChatMessageResponse(
        session_id=session.id,
        reply=assistant_reply,
        suggested_actions=suggested_actions or ["Reduce Budget", "Weather Safe Options", "Cheaper Stays"],
        retrieved_sources=sources
    )
