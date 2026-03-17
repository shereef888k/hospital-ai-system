from app.services.rule_engine import check_emergency_rules, score_based_triage, normalize_symptoms
from app.services.ml_service import predict_from_ml
from app.database import SessionLocal
from app.models.patient_record import PatientRecord
from ml.symptom_normalizer import extract_symptoms


def clean_input(age: int, symptoms: list[str], duration_days: int):
    if age < 0:
        age = 0
    if duration_days < 0:
        duration_days = 0

    cleaned_symptoms = [s.strip() for s in symptoms if s and s.strip()]
    normalized_symptoms = list(normalize_symptoms(cleaned_symptoms))

    return age, normalized_symptoms, duration_days


def save_patient_record(
    age: int,
    gender: str,
    symptoms: list[str],
    duration_days: int,
    result: dict,
):
    db = SessionLocal()
    try:
        record = PatientRecord(
            age=age,
            gender=gender,
            symptoms=", ".join(symptoms),
            duration_days=duration_days,
            urgency=result.get("urgency"),
            department=result.get("department"),
            score=result.get("score") if result.get("score") is not None else 0,
        )
        db.add(record)
        db.commit()
    finally:
        db.close()


def predict_triage(age: int, gender: str, symptoms: list[str], duration_days: int):
    age, symptoms, duration_days = clean_input(age, symptoms, duration_days)

    emergency_result = check_emergency_rules(symptoms)
    if emergency_result:
        save_patient_record(age, gender, symptoms, duration_days, emergency_result)
        return emergency_result

    score_result = score_based_triage(
        age=age,
        symptoms=symptoms,
        duration_days=duration_days,
    )

    try:
        ml_result = predict_from_ml(
            age=age,
            gender=gender,
            symptoms=symptoms,
            duration_days=duration_days,
        )
        score_result["ml_department"] = ml_result.get("department")
        score_result["confidence"] = ml_result.get("confidence")
    except Exception:
        score_result["ml_department"] = None
        score_result["confidence"] = None

    save_patient_record(age, gender, symptoms, duration_days, score_result)
    return score_result


def predict_triage_from_text(text: str, age: int, gender: str, duration_days: int):
    detected_symptoms = extract_symptoms(text)

    if not detected_symptoms:
        return {
            "urgency": "Unknown",
            "department": "OPD",
            "advice": "Could not clearly identify symptoms. Please describe more.",
            "source": "text_parser",
            "score": None,
            "confidence": None,
            "factors": [],
            "detected_symptoms": [],
        }

    result = predict_triage(
        age=age,
        gender=gender,
        symptoms=detected_symptoms,
        duration_days=duration_days,
    )

    result["detected_symptoms"] = detected_symptoms
    return result