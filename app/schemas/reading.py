from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReadingBase(BaseModel):
    """Atributos base de una lectura de sensor."""

    value: float
    unit: str = Field("C", examples=["C", "F", "K"])


class ReadingCreate(ReadingBase):
    """Esquema para registrar una nueva lectura (POST)."""

    sensor_id: int


class ReadingResponse(ReadingBase):
    """Esquema de respuesta para las lecturas de sensor."""

    id: int
    sensor_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)