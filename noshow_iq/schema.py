# noshow_iq/schema.py
from pydantic import BaseModel, Field


class Appointment(BaseModel):
    Gender: str
    Age: int = Field(ge=0, le=110)
    scheduled_day: str
    appointment_day: str
    Scholarship: int = 0
    hypertension: int = 0
    Diabetes: int = 0
    Alcoholism: int = 0
    handicap: int = 0
    sms_received: int = 0
