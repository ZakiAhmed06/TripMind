from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import CrowdPredictionRequest, CrowdPredictionResponse
from backend.app.ml.crowd_engine import predict_crowd

router = APIRouter(prefix="/crowd", tags=["ML Crowd Prediction"])


@router.post("/predict", response_model=CrowdPredictionResponse)
def estimate_crowd_level(req: CrowdPredictionRequest):
    try:
        result = predict_crowd(req)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Crowd estimation error: {str(e)}"
        )
