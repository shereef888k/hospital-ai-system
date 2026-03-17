from sqlalchemy import Column, Integer, String
from app.database import Base


class PatientRecord(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)
    symptoms = Column(String)
    duration_days = Column(Integer)
    urgency = Column(String)
    department = Column(String)
    score = Column(Integer)