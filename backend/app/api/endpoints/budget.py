from fastapi import APIRouter, HTTPException, status
from backend.app.schemas import BudgetPredictionRequest, BudgetPredictionResponse, ExpenseBreakdown
from backend.app.ml.budget_engine import predict_expense

router = APIRouter(prefix="/budget", tags=["ML Budget Prediction"])


@router.post("/predict", response_model=BudgetPredictionResponse)
def predict_travel_budget(req: BudgetPredictionRequest):
    try:
        result = predict_expense(req)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Budget prediction error: {str(e)}"
        )


@router.post("/breakdown", response_model=ExpenseBreakdown)
def get_expense_breakdown(req: BudgetPredictionRequest):
    try:
        result = predict_expense(req)
        return result.breakdown
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Expense breakdown calculation error: {str(e)}"
        )
