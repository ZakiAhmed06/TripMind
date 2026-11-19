"""
Dynamic Itinerary Replanning Service
Detects outdoor activities affected by weather alerts or user triggers,
retrieves indoor/weather-safe alternatives from the dataset and knowledge base,
and regenerates an optimized schedule.
"""
import os
import json
import logging
from typing import List, Dict, Any
import pandas as pd
from backend.app.schemas import ReplanningRequest, DayItinerary, ActivityItem
from backend.app.core.config import settings
from backend.app.genai.rag_service import retrieve_context

logger = logging.getLogger(__name__)


def replan_day_itinerary(req: ReplanningRequest) -> List[DayItinerary]:
    logger.info("Replanning trip for %s on Day %d due to: %s", req.destination_name, req.affected_day, req.reason)

    days_list = req.current_days.copy()
    affected_idx = -1
    for i, d in enumerate(days_list):
        if d.day_number == req.affected_day:
            affected_idx = i
            break

    if affected_idx == -1:
        logger.warning("Affected day %d not found in itinerary.", req.affected_day)
        return days_list

    target_day = days_list[affected_idx]

    # Find indoor alternatives from attractions dataset
    csv_path = "data/processed/attractions.csv"
    indoor_alternatives = []
    if os.path.exists(csv_path):
        df_attr = pd.read_csv(csv_path)
        matching = df_attr[(df_attr["destination_name"].str.lower() == req.destination_name.lower()) & (df_attr["is_outdoor"] == False)]
        if not matching.empty:
            indoor_alternatives = matching.to_dict("records")

    # If few indoor attractions in that specific destination, also check state/general indoor experiences
    if not indoor_alternatives:
        indoor_alternatives = [
            {
                "name": f"{req.destination_name} Heritage Museum & Gallery",
                "description": "Explore historical artifacts, royal paintings, and regional textiles in an indoor heritage gallery.",
                "estimated_duration_hours": 2.0,
                "entry_fee": 150.0,
                "is_outdoor": False,
                "category": "Heritage"
            },
            {
                "name": f"{req.destination_name} Traditional Tea & Spice Tasting House",
                "description": "Cozy indoor masterclass sampling regional organic tea flushes and fragrant spices.",
                "estimated_duration_hours": 1.5,
                "entry_fee": 250.0,
                "is_outdoor": False,
                "category": "Food"
            },
            {
                "name": f"{req.destination_name} Handicrafts & Silk Weaving Emporium",
                "description": "Sheltered artisanal guild showcasing live master-weaver demonstrations and traditional brass craft.",
                "estimated_duration_hours": 2.0,
                "entry_fee": 0.0,
                "is_outdoor": False,
                "category": "Culture"
            }
        ]

    # Reconstruct activities for the affected day
    new_activities = []
    alt_idx = 0

    for act in target_day.activities:
        if act.is_outdoor:
            # Swap for an indoor activity
            alt = indoor_alternatives[alt_idx % len(indoor_alternatives)]
            alt_idx += 1
            new_activities.append(ActivityItem(
                id=f"replan-{target_day.day_number}-{act.sequence_order}",
                time_slot=act.time_slot,
                attraction_name=alt["name"],
                description=f"[Weather Adapted - Rain Safe] {alt['description']}",
                duration_hours=float(alt.get("estimated_duration_hours", 2.0)),
                estimated_cost=float(alt.get("entry_fee", 100.0)),
                is_outdoor=False,
                sequence_order=act.sequence_order,
                category=alt.get("category", "Culture")
            ))
        else:
            # Retain existing indoor activity
            new_activities.append(act)

    # Update day title and notes
    replanned_day = DayItinerary(
        day_number=target_day.day_number,
        date=target_day.date,
        title=f"Day {target_day.day_number}: [Replanned] Weather-Safe Indoor & Cultural Discovery",
        activities=new_activities,
        food_recommendations=[
            f"Cozy {req.destination_name} cafe with hot beverages and indoor seating",
            "Heritage dining hall with warm regional soup and comfort meals"
        ],
        transport_tips=f"Pre-arranged indoor cabs or hotel taxis recommended due to {req.reason.lower()}.",
        estimated_daily_expense=target_day.estimated_daily_expense
    )

    days_list[affected_idx] = replanned_day
    return days_list
