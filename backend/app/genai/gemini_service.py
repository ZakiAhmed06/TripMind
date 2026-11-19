"""
Gemini Generative AI Integration & Itinerary Generator
Uses Google GenAI SDK (Gemini 2.5 Flash) with structured JSON generation,
grounded RAG context, and deterministic offline fallback.
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
import pandas as pd
from backend.app.core.config import settings
from backend.app.schemas import (
    ItineraryGenerateRequest,
    ItineraryResponse,
    DayItinerary,
    ActivityItem,
    ExpenseBreakdown,
    BudgetPredictionRequest
)
from backend.app.ml.budget_engine import predict_expense
from backend.app.genai.rag_service import retrieve_context

logger = logging.getLogger(__name__)

# Initialize GenAI client if API key is present
_genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        _genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Google GenAI client initialized with model %s", settings.GEMINI_MODEL)
    except Exception as e:
        logger.warning("Could not initialize google-genai client: %s", e)


def generate_structured_itinerary(req: ItineraryGenerateRequest) -> ItineraryResponse:
    """
    Generates a structured, validated day-wise travel itinerary using Gemini AI with ML-validated budget.
    """
    # 1. First obtain ML-predicted expenses for sanity and baseline
    budget_req = BudgetPredictionRequest(
        destination_name=req.destination_name,
        duration_days=req.duration_days,
        travellers_count=req.travellers_count,
        transport_mode=req.transport_mode,
        hotel_category=req.accommodation_category,
        season="Peak" if req.start_date and any(m in req.start_date for m in ["10", "11", "12", "01"]) else "Moderate",
        food_preference=req.food_preference,
        sightseeing_count=req.duration_days * 2
    )
    ml_budget_result = predict_expense(budget_req)
    predicted_breakdown = ml_budget_result.breakdown
    estimated_total = predicted_breakdown.total

    # 2. Retrieve grounded knowledge from RAG for the destination
    rag_chunks = retrieve_context(f"{req.destination_name} tourist attractions travel tips culture", top_k=3)
    rag_context_text = "\n\n".join([f"[{c['section']}] {c['content']}" for c in rag_chunks])

    # 3. Try calling Gemini if API key is configured
    itinerary_data = None
    source = "Gemini 2.5 Flash + ML Engine"

    if _genai_client and settings.GEMINI_API_KEY:
        try:
            prompt = f"""You are TripMind AI, an expert travel planner.
Generate a comprehensive, realistic day-wise travel itinerary for:
Destination: {req.destination_name}
Starting City (Origin): {req.origin}
Duration: {req.duration_days} days
Number of Travellers: {req.travellers_count}
Total Budget: INR {req.budget}
Interests: {', '.join(req.travel_interests)}
Transport: {req.transport_mode}
Accommodation: {req.accommodation_category}
Food Preference: {req.food_preference}

GROUNDED TRAVEL KNOWLEDGE BASE:
{rag_context_text}

INSTRUCTIONS:
Output STRICTLY valid JSON with no markdown formatting, no code fences, adhering to this structure:
{{
  "days": [
    {{
      "day_number": 1,
      "title": "Arrival & Initial Exploration",
      "activities": [
        {{
          "time_slot": "Morning",
          "attraction_name": "Specific Attraction Name",
          "description": "Engaging 1-2 sentence description",
          "duration_hours": 2.5,
          "estimated_cost": 200,
          "is_outdoor": true,
          "sequence_order": 1,
          "category": "Sightseeing"
        }}
      ],
      "food_recommendations": ["Authentic local breakfast place", "Traditional dinner spot"],
      "transport_tips": "Advice for local transit.",
      "estimated_daily_expense": 2500
    }}
  ],
  "travel_tips": [
    "Tip 1", "Tip 2", "Tip 3"
  ]
}}
Ensure exactly {req.duration_days} days are provided with 3 to 4 activities per day."""

            response = _genai_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
            )
            text_resp = response.text.strip()
            # Remove potential markdown json tags
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:]
            if text_resp.endswith("```"):
                text_resp = text_resp[:-3]
            itinerary_data = json.loads(text_resp.strip())
            logger.info("Successfully generated itinerary via Gemini API for %s", req.destination_name)
        except Exception as e:
            logger.warning("Gemini API call failed (%s), switching to robust fallback generator.", e)
            itinerary_data = None

    # 4. Fallback generator if Gemini is unavailable or not configured
    if not itinerary_data:
        source = "TripMind Intelligent Algorithmic Planner + ML Engine"
        itinerary_data = generate_fallback_itinerary(req, rag_chunks)

    # 5. Pydantic validation & structure assembly
    parsed_days = []
    for day_item in itinerary_data.get("days", []):
        parsed_activities = []
        for seq, act in enumerate(day_item.get("activities", []), start=1):
            parsed_activities.append(ActivityItem(
                id=f"act-d{day_item.get('day_number', 1)}-{seq}",
                time_slot=act.get("time_slot", "Morning"),
                attraction_name=act.get("attraction_name", f"{req.destination_name} Landmark"),
                description=act.get("description", "Enjoy scenic sightseeing and local culture."),
                duration_hours=float(act.get("duration_hours", 2.0)),
                estimated_cost=float(act.get("estimated_cost", 100.0)),
                is_outdoor=bool(act.get("is_outdoor", True)),
                sequence_order=int(act.get("sequence_order", seq)),
                category=act.get("category", "Sightseeing")
            ))
        
        parsed_days.append(DayItinerary(
            day_number=int(day_item.get("day_number", 1)),
            title=day_item.get("title", f"Day {day_item.get('day_number', 1)} Highlights"),
            activities=parsed_activities,
            food_recommendations=day_item.get("food_recommendations", ["Local cuisine specialties"]),
            transport_tips=day_item.get("transport_tips", "Cabs and auto-rickshaws available."),
            estimated_daily_expense=round(estimated_total / max(1, req.duration_days), 2)
        ))

    return ItineraryResponse(
        destination_name=req.destination_name,
        origin=req.origin,
        duration_days=req.duration_days,
        travellers_count=req.travellers_count,
        total_budget=req.budget,
        estimated_total_expense=estimated_total,
        expense_breakdown=predicted_breakdown,
        days=parsed_days,
        travel_tips=itinerary_data.get("travel_tips", [
            f"Start your days early in {req.destination_name} to avoid afternoon peak crowds.",
            "Carry valid government ID proofs for entry permits and monument verification.",
            "Keep emergency contact numbers and offline maps handy."
        ]),
        source=source
    )


def generate_fallback_itinerary(req: ItineraryGenerateRequest, rag_chunks: list) -> dict:
    """
    Deterministic, high-quality fallback generator utilizing the attractions dataset and RAG knowledge.
    """
    csv_path = "data/processed/attractions.csv"
    attractions_list = []
    if os.path.exists(csv_path):
        df_attr = pd.read_csv(csv_path)
        matching = df_attr[df_attr["destination_name"].str.lower() == req.destination_name.lower()]
        if not matching.empty:
            attractions_list = matching.to_dict("records")

    time_slots = ["Morning", "Afternoon", "Evening", "Night"]
    days = []

    day_themes = [
        "Arrival, Heritage Landmarks & Sunset Views",
        "Scenic Nature Trails & Cultural Heritage",
        "Adventure Activities & Traditional Food Exploration",
        "Local Arts, Handloom Markets & Leisure Walks",
        "Valley Panoramas & Scenic Overlooks",
        "Spiritual Shrines & Riverfront Discovery",
        "Farewell Stroll & Souvenir Shopping"
    ]

    for day_idx in range(1, req.duration_days + 1):
        theme = day_themes[(day_idx - 1) % len(day_themes)]
        day_activities = []
        
        for slot_idx, slot in enumerate(["Morning", "Afternoon", "Evening"]):
            # Pick attraction from dataset if available
            attr_name = f"{req.destination_name} Landmark {slot_idx + 1}"
            attr_desc = f"Experience panoramic views and rich regional heritage in {req.destination_name}."
            is_outdoor = True
            duration = 2.0
            fee = 50.0

            if attractions_list:
                item = attractions_list[((day_idx - 1) * 3 + slot_idx) % len(attractions_list)]
                attr_name = item["name"]
                attr_desc = item["description"]
                is_outdoor = bool(item["is_outdoor"])
                duration = float(item["estimated_duration_hours"])
                fee = float(item["entry_fee"])

            day_activities.append({
                "time_slot": slot,
                "attraction_name": attr_name,
                "description": attr_desc,
                "duration_hours": duration,
                "estimated_cost": fee,
                "is_outdoor": is_outdoor,
                "sequence_order": slot_idx + 1,
                "category": "Sightseeing"
            })

        days.append({
            "day_number": day_idx,
            "title": f"Day {day_idx}: {theme}",
            "activities": day_activities,
            "food_recommendations": [
                f"Traditional {req.destination_name} breakfast eatery",
                "Authentic thali restaurant in the market square"
            ],
            "transport_tips": f"Auto-rickshaws and shared jeeps operate frequently between {req.destination_name} sights.",
            "estimated_daily_expense": 2400
        })

    return {
        "days": days,
        "travel_tips": [
            f"Reserve monument tickets early in {req.destination_name} for smooth entry.",
            f"Try local specialty snacks and seasonal tea brews during evening strolls.",
            "Carry cash as smaller local vendors and hill shacks may have patchy digital network."
        ]
    }
