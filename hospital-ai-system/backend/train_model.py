import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

print("Loading dataset...")

df = pd.read_csv("patient_data.csv")

print("Dataset loaded")

X = df[["age", "gender", "symptoms", "duration_days"]]

y_urgency = df["urgency"]
y_department = df["department"]

preprocessor = ColumnTransformer(
    transformers=[
        ("text", TfidfVectorizer(), "symptoms"),
        ("gender", OneHotEncoder(), ["gender"]),
        ("num", "passthrough", ["age", "duration_days"])
    ]
)

urgency_model = Pipeline([
    ("prep", preprocessor),
    ("model", RandomForestClassifier())
])

department_model = Pipeline([
    ("prep", preprocessor),
    ("model", RandomForestClassifier())
])

print("Training models...")

urgency_model.fit(X, y_urgency)
department_model.fit(X, y_department)

joblib.dump(urgency_model, "urgency_model.pkl")
joblib.dump(department_model, "department_model.pkl")

print("Models trained and saved successfully")