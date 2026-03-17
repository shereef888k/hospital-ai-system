from typing import List, Tuple, Dict, Optional


def normalize_symptoms(symptoms: List[str]) -> set[str]:
    symptom_aliases = {
        "shortness of breath": "shortness of breath",
        "breathlessness": "shortness of breath",
        "breathing problem": "breathing difficulty",
        "breathing difficulty": "breathing difficulty",
        "tight chest": "chest pain",
        "chest tightness": "chest pain",
        "heart pain": "chest pain",
        "fainting": "unconsciousness",
        "passed out": "unconsciousness",
        "heavy bleeding": "severe bleeding",
        "bleeding heavily": "severe bleeding",
        "feeling dizzy": "dizziness",
        "stomach pain": "abdominal pain",
    }

    normalized = set()
    for symptom in symptoms:
        cleaned = symptom.lower().strip()
        normalized.add(symptom_aliases.get(cleaned, cleaned))
    return normalized


def calculate_risk_score(age: int, symptoms: List[str], duration_days: int) -> Tuple[int, List[str]]:
    symptom_set = normalize_symptoms(symptoms)
    score = 0
    factors: List[str] = []

    # Basic validation
    if age < 0:
        age = 0
    if duration_days < 0:
        duration_days = 0

    # Age score
    if age <= 5:
        score += 3
        factors.append("Very young child risk")
    elif age <= 12:
        score += 2
        factors.append("Child age risk")
    elif age >= 75:
        score += 4
        factors.append("Very high elderly age risk")
    elif age >= 60:
        score += 3
        factors.append("Elderly age risk")

    # Duration score
    if duration_days >= 30:
        score += 4
        factors.append("Symptoms lasting 30+ days")
    elif duration_days >= 15:
        score += 3
        factors.append("Symptoms lasting 15+ days")
    elif duration_days >= 8:
        score += 2
        factors.append("Symptoms lasting 8+ days")
    elif duration_days >= 3:
        score += 1
        factors.append("Symptoms lasting 3+ days")

    # Symptom weights
    symptom_scores = {
        "fever": 2,
        "cough": 1,
        "vomiting": 2,
        "dizziness": 2,
        "headache": 1,
        "chest pain": 5,
        "breathing difficulty": 5,
        "shortness of breath": 5,
        "sweating": 2,
        "rash": 1,
        "itching": 1,
        "fatigue": 1,
        "abdominal pain": 3,
        "dehydration": 3,
        "unconsciousness": 10,
        "severe bleeding": 10,
        "palpitations": 3,
        "confusion": 4,
        "blurred vision": 3,
        "weakness": 3,
    }

    for symptom in symptom_set:
        if symptom in symptom_scores:
            score += symptom_scores[symptom]
            factors.append(f"Symptom present: {symptom}")

    # Combination bonuses
    if "chest pain" in symptom_set and "sweating" in symptom_set:
        score += 4
        factors.append("High-risk combination: chest pain + sweating")

    if "chest pain" in symptom_set and (
        "breathing difficulty" in symptom_set or "shortness of breath" in symptom_set
    ):
        score += 5
        factors.append("High-risk combination: chest pain + breathing problem")

    if "fever" in symptom_set and "cough" in symptom_set and duration_days >= 7:
        score += 3
        factors.append("Persistent fever + cough")

    if "vomiting" in symptom_set and "dizziness" in symptom_set:
        score += 3
        factors.append("Vomiting with dizziness")

    if "confusion" in symptom_set and "weakness" in symptom_set:
        score += 4
        factors.append("Neurological high-risk combination")

    if "abdominal pain" in symptom_set and "vomiting" in symptom_set:
        score += 2
        factors.append("Abdominal pain with vomiting")

    return score, factors


def urgency_from_score(score: int) -> str:
    if score >= 12:
        return "Emergency"
    if score >= 8:
        return "High"
    if score >= 4:
        return "Medium"
    return "Low"


def suggested_department(symptoms: List[str]) -> str:
    symptom_set = normalize_symptoms(symptoms)

    # Priority order matters
    if "unconsciousness" in symptom_set or "severe bleeding" in symptom_set:
        return "Emergency"
    if "chest pain" in symptom_set:
        return "Cardiology"
    if "breathing difficulty" in symptom_set or "shortness of breath" in symptom_set:
        return "Pulmonology"
    if "confusion" in symptom_set or "weakness" in symptom_set or "dizziness" in symptom_set or "headache" in symptom_set:
        return "Neurology"
    if "rash" in symptom_set or "itching" in symptom_set:
        return "Dermatology"
    if "abdominal pain" in symptom_set or "vomiting" in symptom_set:
        return "Gastroenterology"
    return "General Medicine"


def advice_from_urgency(urgency: str) -> str:
    if urgency == "Emergency":
        return "Immediate emergency care required."
    if urgency == "High":
        return "Urgent doctor consultation recommended."
    if urgency == "Medium":
        return "Consult a doctor soon."
    return "Routine consultation is sufficient."


def check_emergency_rules(symptoms: List[str]) -> Optional[Dict]:
    symptom_set = normalize_symptoms(symptoms)

    if "unconsciousness" in symptom_set:
        return {
            "urgency": "Emergency",
            "department": "Emergency",
            "advice": "Immediate emergency care required.",
            "source": "rule_engine",
            "score": 15,
            "factors": ["Critical red flag: unconsciousness"],
        }

    if "severe bleeding" in symptom_set:
        return {
            "urgency": "Emergency",
            "department": "Emergency",
            "advice": "Control bleeding and seek immediate emergency care.",
            "source": "rule_engine",
            "score": 15,
            "factors": ["Critical red flag: severe bleeding"],
        }

    if "chest pain" in symptom_set and (
        "breathing difficulty" in symptom_set or "shortness of breath" in symptom_set
    ):
        return {
            "urgency": "Emergency",
            "department": "Emergency",
            "advice": "Possible cardiac or respiratory emergency. Seek immediate care.",
            "source": "rule_engine",
            "score": 15,
            "factors": ["Critical red flag: chest pain with breathing difficulty"],
        }

    return None


def score_based_triage(age: int, symptoms: List[str], duration_days: int) -> Dict:
    score, factors = calculate_risk_score(
        age=age,
        symptoms=symptoms,
        duration_days=duration_days,
    )
    urgency = urgency_from_score(score)
    department = suggested_department(symptoms)
    advice = advice_from_urgency(urgency)

    return {
        "urgency": urgency,
        "department": department,
        "advice": advice,
        "source": "scoring_engine",
        "score": score,
        "factors": factors,
    }