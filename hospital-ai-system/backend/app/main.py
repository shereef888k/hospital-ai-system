from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.triage import router as triage_router
from app.routes.patients import router as patients_router
from app.routes.admin import router as admin_router

from app.database import engine, Base
from app.models.patient_record import PatientRecord

app = FastAPI(title="Hospital AI System")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://hospital-ai-system-gaz9.vercel.app",
        "https://hospital-ai-system-theta.vercel.app",
        "https://hospital-ai-system-m7eh.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage_router)
app.include_router(patients_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"message": "Hospital AI System API running"}