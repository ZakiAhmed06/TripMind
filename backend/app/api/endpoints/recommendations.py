from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import RecommendationRequest, RecommendationResponse
from backend.app.ml.recommendation_engine import get_recommendations

router = APIRouter(prefix="/recommendations", tags=["ML Recommendations"])


@router.post("", response_model=RecommendationResponse)
def recommend_destinations(req: RecommendationRequest):
    try:
        ranked = get_recommendations(req, top_k=12)
        return RecommendationResponse(
            recommendations=ranked,
            total_found=len(ranked)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating destination recommendations: {str(e)}"
        )
