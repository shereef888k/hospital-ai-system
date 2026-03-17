from fastapi import APIRouter, HTTPException
from app.models.schemas import TriageRequest, TriageResponse, TextTriageRequest
from app.services.triage_service import predict_triage, predict_triage_from_text

router = APIRouter(
    prefix="/triage",
    tags=["Triage"]
)

@router.get("/")
def check_triage():
    return {"message": "Triage route working"}

@router.post("/predict", response_model=TriageResponse)
def triage_predict(data: TriageRequest):
    try:
        return predict_triage(
            age=data.age,
            gender=data.gender,
            symptoms=data.symptoms,
            duration_days=data.duration_days,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text")
def triage_text(data: TextTriageRequest):
    try:
        return predict_triage_from_text(
            text=data.text,
            age=data.age,
            gender=data.gender,
            duration_days=data.duration_days,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))