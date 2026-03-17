from pathlib import Path
from typing import Optional

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
ML_DIR = BASE_DIR / "ml"

URGENCY_MODEL_PATH = ML_DIR / "urgency_model.pkl"
DEPARTMENT_MODEL_PATH = ML_DIR / "department_model.pkl"

urgency_model = None
department_model = None


def load_models():
    global urgency_model, department_model

    if urgency_model is None and URGENCY_MODEL_PATH.exists():
        urgency_model = joblib.load(URGENCY_MODEL_PATH)

    if department_model is None and DEPARTMENT_MODEL_PATH.exists():
        department_model = joblib.load(DEPARTMENT_MODEL_PATH)


def clean_ml_input(age: int, gender: str, symptoms: list[str], duration_days: int):
    if age < 0:
        age = 0
    if duration_days < 0:
        duration_days = 0

    gender = (gender or "unknown").strip().lower()
    symptoms = [s.strip() for s in symptoms if s and s.strip()]

    return age, gender, symptoms, duration_days


def get_confidence(model, input_df) -> Optional[float]:
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        return round(float(max(probs)), 3)
    return None


def advice_from_urgency(urgency: str) -> str:
    if urgency == "Emergency":
        return "Immediate emergency care required."
    if urgency == "High":
        return "Immediate medical attention recommended."
    if urgency == "Medium":
        return "Consult doctor soon."
    return "Routine consultation is sufficient."


def predict_from_ml(age: int, gender: str, symptoms: list[str], duration_days: int):
    load_models()

    if urgency_model is None or department_model is None:
        raise FileNotFoundError("ML model files not found in backend/ml")

    age, gender, symptoms, duration_days = clean_ml_input(
        age, gender, symptoms, duration_days
    )

    symptoms_text = ", ".join(symptoms)

    input_df = pd.DataFrame(
        [
            {
                "age": age,
                "gender": gender,
                "symptoms": symptoms_text,
                "duration_days": duration_days,
            }
        ]
    )

    urgency = urgency_model.predict(input_df)[0]
    department = department_model.predict(input_df)[0]
    confidence = get_confidence(urgency_model, input_df)

    return {
        "urgency": urgency,
        "department": department,
        "advice": advice_from_urgency(urgency),
        "source": "ml_model",
        "confidence": confidence,
    }