# symptom_normalizer.py

SYMPTOM_MAP = {
    "chest pain": "chest pain",
    "pain in chest": "chest pain",
    "nenju vedana": "chest pain",
    "നെഞ്ച് വേദന": "chest pain",

    "breathing difficulty": "breathing difficulty",
    "shortness of breath": "breathing difficulty",
    "shwasam muttal": "breathing difficulty",
    "ശ്വാസം മുട്ടൽ": "breathing difficulty",

    "fever": "fever",
    "high fever": "fever",
    "pani": "fever",
    "ജ്വരം": "fever",

    "cough": "cough",
    "chuma": "cough",
    "ചുമ": "cough",

    "headache": "headache",
    "thalavedana": "headache",
    "തലവേദന": "headache",

    "stomach pain": "stomach pain",
    "vayaru vedana": "stomach pain",
    "വയറുവേദന": "stomach pain",
}


def extract_symptoms(text: str):
    text = text.lower()

    detected = []

    for phrase, symptom in SYMPTOM_MAP.items():
        if phrase in text:
            detected.append(symptom)

    return list(set(detected))