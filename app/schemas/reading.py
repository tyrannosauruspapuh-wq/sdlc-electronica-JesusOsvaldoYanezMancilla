# app/schemas.py (o app/schemas/reading.py)
from pydantic import BaseModel, Field


class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"


class SensorReadingOut(SensorReadingIn):
    id: int