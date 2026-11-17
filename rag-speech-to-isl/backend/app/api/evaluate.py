from fastapi import APIRouter, HTTPException
from app.models.schemas import EvaluationRequest, EvaluationResponse
from app.services.evaluation_service import evaluation_service

router = APIRouter(prefix="/api", tags=["Evaluation"])

@router.post("/evaluate", response_model=EvaluationResponse)
def run_evaluation(request: EvaluationRequest):
    try:
        return evaluation_service.run_evaluation(
            use_rag=request.use_rag,
            test_limit=request.test_limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation pipeline failed: {str(e)}")
