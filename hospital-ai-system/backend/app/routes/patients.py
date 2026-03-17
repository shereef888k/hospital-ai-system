from fastapi import APIRouter
from app.database import SessionLocal
from app.models.patient_record import PatientRecord

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get("/")
def get_patients():
    db = SessionLocal()
    try:
        patients = db.query(PatientRecord).all()

        return [
            {
                "id": patient.id,
                "age": patient.age,
                "gender": patient.gender,
                "symptoms": patient.symptoms,
                "duration_days": patient.duration_days,
                "urgency": patient.urgency,
                "department": patient.department,
                "score": patient.score,
            }
            for patient in patients
        ]
    finally:
        db.close()