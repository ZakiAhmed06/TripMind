import os
import joblib
import logging
import pandas as pd
from typing import Dict, Any
from backend.app.schemas import BudgetPredictionRequest, BudgetPredictionResponse, ExpenseBreakdown

logger = logging.getLogger(__name__)

MODEL_PATH = "backend/trained_models/budget_model.joblib"
_budget_pipeline = None


def get_budget_model():
    global _budget_pipeline
    if _budget_pipeline is None:
        if os.path.exists(MODEL_PATH):
            logger.info("Loading saved budget model from %s", MODEL_PATH)
            _budget_pipeline = joblib.load(MODEL_PATH)
        else:
            logger.warning("Saved budget model not found at %s. Retraining now...", MODEL_PATH)
            from backend.app.ml.train_budget import train_budget_model
            _budget_pipeline, _ = train_budget_model()
    return _budget_pipeline


def predict_expense(req: BudgetPredictionRequest) -> BudgetPredictionResponse:
    model = get_budget_model()

    input_df = pd.DataFrame([{
        "destination_category": req.destination_category or "Mountains",
        "transport_mode": req.transport_mode,
        "hotel_category": req.hotel_category,
        "season": req.season,
        "food_preference": req.food_preference,
        "duration_days": req.duration_days,
        "travellers_count": req.travellers_count,
        "sightseeing_count": req.sightseeing_count
    }])

    raw_prediction = float(model.predict(input_df)[0])
    raw_prediction = max(1500.0 * req.duration_days * req.travellers_count, raw_prediction)

    # Itemized Breakdown Ratio Calibration
    # Calibrated proportional division according to transport, hotel tier, days and count
    transport_weight_map = {"Flight": 0.38, "Cab": 0.30, "Train": 0.20, "Bus": 0.14}
    hotel_weight_map = {"Luxury (4/5-star)": 0.40, "Standard (3-star)": 0.30, "Budget": 0.20}
    
    tw = transport_weight_map.get(req.transport_mode, 0.25)
    hw = hotel_weight_map.get(req.hotel_category, 0.30)
    fw = 0.20  # Food
    sw = 0.15  # Sightseeing
    mw = 0.10  # Misc

    # Normalize proportions
    total_w = tw + hw + fw + sw + mw
    tw, hw, fw, sw, mw = tw / total_w, hw / total_w, fw / total_w, sw / total_w, mw / total_w

    transportation = round(raw_prediction * tw, 2)
    accommodation = round(raw_prediction * hw, 2)
    food = round(raw_prediction * fw, 2)
    sightseeing = round(raw_prediction * sw, 2)
    miscellaneous = round(raw_prediction * mw, 2)
    
    total = round(transportation + accommodation + food + sightseeing + miscellaneous, 2)
    per_person = round(total / max(1, req.travellers_count), 2)

    breakdown = ExpenseBreakdown(
        transportation=transportation,
        accommodation=accommodation,
        food=food,
        sightseeing=sightseeing,
        miscellaneous=miscellaneous,
        total=total,
        currency="INR"
    )

    return BudgetPredictionResponse(
        destination=req.destination_name,
        duration_days=req.duration_days,
        travellers_count=req.travellers_count,
        predicted_total_expense=total,
        per_person_expense=per_person,
        breakdown=breakdown,
        model_used="RandomForestRegressor (120 Estimators)",
        is_model_trained=True,
        confidence_note="Calculated via Scikit-Learn Random Forest Regressor with backend sanity verification."
    )
