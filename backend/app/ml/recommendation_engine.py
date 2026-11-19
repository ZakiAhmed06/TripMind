import os
import joblib
import logging
from typing import List, Optional
from backend.app.schemas import RecommendationRequest, DestinationRecommendation

logger = logging.getLogger(__name__)

MODEL_PATH = "backend/trained_models/recommendation_model.joblib"
_model_instance = None


def get_recommendation_model():
    global _model_instance
    if _model_instance is None:
        if os.path.exists(MODEL_PATH):
            logger.info("Loading saved recommendation model from %s", MODEL_PATH)
            _model_instance = joblib.load(MODEL_PATH)
        else:
            logger.warning("Saved recommendation model not found at %s. Initializing fresh model...", MODEL_PATH)
            from backend.app.ml.train_recommendation import train_and_save
            _model_instance, _ = train_and_save()
    return _model_instance


def get_recommendations(req: RecommendationRequest, top_k: int = 12) -> List[DestinationRecommendation]:
    model = get_recommendation_model()
    raw_ranked = model.rank(
        user_interests=req.interests,
        budget=req.budget,
        duration_days=req.duration_days,
        travellers_count=req.travellers_count,
        state_filter=req.state,
        top_k=top_k
    )
    
    output = []
    for item in raw_ranked:
        output.append(DestinationRecommendation(**item))
    return output
