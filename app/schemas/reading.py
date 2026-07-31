from datetime import datetime

from pydantic import BaseModel, Field


class SensorReadingIn(BaseModel):
    sensor_id: str = Field(..., examples=["TEMP-01"])
    value: float
    unit: str = "C"

class SensorReadingUpdate(BaseModel):
    value: float | None = None
    unit: str | None = None

class SensorReadingOut(SensorReadingIn):
    id: int
    created_at: datetime

    # Permite que Pydantic lea directamente los objetos ORM de SQLAlchemy
    model_config = {"from_attributes": True}