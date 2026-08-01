from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ReadingBase(BaseModel):
    """Atributos base de una lectura de sensor."""

    value: float
    unit: str = Field("C", examples=["C", "F", "K"])

    @field_validator("value")
    @classmethod
    def validate_physical_value(cls, v: float) -> float:
        """Validación física básica: no puede ser inferior al cero absoluto en °C."""
        if v < -273.15:
            raise ValueError(
                "El valor no puede ser inferior al cero absoluto (-273.15 °C)"
            )
        return v


class ReadingCreate(ReadingBase):
    """Esquema para registrar una nueva lectura (POST)."""

    sensor_id: int


class ReadingResponse(ReadingBase):
    """Esquema de respuesta para las lecturas de sensor."""

    id: int
    sensor_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)