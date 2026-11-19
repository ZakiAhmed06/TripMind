import os
import joblib
import logging
import pandas as pd
from backend.app.schemas import CrowdPredictionRequest, CrowdPredictionResponse

logger = logging.getLogger(__name__)

MODEL_PATH = "backend/trained_models/crowd_model.joblib"
_crowd_pipeline = None


def get_crowd_model():
    global _crowd_pipeline
    if _crowd_pipeline is None:
        if os.path.exists(MODEL_PATH):
            logger.info("Loading saved crowd model from %s", MODEL_PATH)
            _crowd_pipeline = joblib.load(MODEL_PATH)
        else:
            logger.warning("Saved crowd model not found at %s. Retraining now...", MODEL_PATH)
            from backend.app.ml.train_crowd import train_crowd_model
            _crowd_pipeline, _ = train_crowd_model()
    return _crowd_pipeline


def predict_crowd(req: CrowdPredictionRequest) -> CrowdPredictionResponse:
    model = get_crowd_model()

    input_df = pd.DataFrame([{
        "month": req.month,
        "day_of_week": req.day_of_week,
        "is_weekend": 1 if req.is_weekend else 0,
        "is_public_holiday": 1 if req.is_public_holiday else 0,
        "season": req.season or "Winter"
    }])

    predicted_level = str(model.predict(input_df)[0])

    # Probability estimation for score
    try:
        probas = model.predict_proba(input_df)[0]
        classes = list(model.named_steps["classifier"].classes_)
        high_idx = classes.index("High") if "High" in classes else 0
        med_idx = classes.index("Medium") if "Medium" in classes else 0
        crowd_score = round(float(probas[high_idx] * 0.9 + probas[med_idx] * 0.5), 2)
    except Exception:
        score_map = {"Low": 0.3, "Medium": 0.6, "High": 0.85}
        crowd_score = score_map.get(predicted_level, 0.5)

    if predicted_level == "High":
        recommendation = "Heavy tourist traffic expected. Pre-book monument entries and plan early morning visits before 9:00 AM."
        best_time = "Weekdays, early morning 7:30 AM - 9:30 AM"
    elif predicted_level == "Medium":
        recommendation = "Moderate footfall. Standard visiting queues; ideal balance of pleasant atmosphere and activity availability."
        best_time = "Forenoon or late afternoon sunset hours"
    else:
        recommendation = "Low crowds. Peaceful sightseeing conditions, minimal queues, and easier photography opportunities."
        best_time = "Anytime during standard operating hours"

    return CrowdPredictionResponse(
        destination=req.destination_name,
        month=req.month,
        crowd_level=predicted_level,
        crowd_score=crowd_score,
        best_time_to_visit=best_time,
        recommendation=recommendation,
        model_used="RandomForestClassifier"
    )
