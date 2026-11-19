from typing import List, Dict, Any
from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.route_optimizer import optimize_attraction_sequence

router = APIRouter(prefix="/routes", tags=["Route Optimization"])


class RouteOptimizationRequest(BaseModel):
    attractions: List[Dict[str, Any]]


@router.post("/optimize")
def optimize_route(req: RouteOptimizationRequest):
    result = optimize_attraction_sequence(req.attractions)
    return result
