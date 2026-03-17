from fastapi import APIRouter
from sqlalchemy import func
from app.database import SessionLocal
from app.models.patient_record import PatientRecord

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def get_admin_stats():
    db = SessionLocal()
    try:
        total_patients = db.query(PatientRecord).count()
        emergency_count = db.query(PatientRecord).filter(PatientRecord.urgency == "Emergency").count()
        high_count = db.query(PatientRecord).filter(PatientRecord.urgency == "High").count()
        medium_count = db.query(PatientRecord).filter(PatientRecord.urgency == "Medium").count()
        low_count = db.query(PatientRecord).filter(PatientRecord.urgency == "Low").count()

        department_counts = (
            db.query(PatientRecord.department, func.count(PatientRecord.id))
            .group_by(PatientRecord.department)
            .all()
        )

        return {
            "total_patients": total_patients,
            "emergency": emergency_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "departments": [
                {"department": dept, "count": count}
                for dept, count in department_counts
            ],
        }
    finally:
        db.close()