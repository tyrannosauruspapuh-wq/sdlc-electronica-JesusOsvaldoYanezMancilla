from pydantic import BaseModel, ConfigDict, Field


class SensorBase(BaseModel):
    """Atributos base compartidos de un sensor."""

    name: str = Field(..., examples=["Sensor de Temperatura Laboratorio"])
    type: str = Field(..., examples=["temperature"])
    unit: str = Field("C", examples=["C", "F", "K", "%", "Pa"])
    min_value: float = Field(-273.15, description="Valor mínimo permitido")
    max_value: float = Field(1000.0, description="Valor máximo permitido")


class SensorCreate(SensorBase):
    """Esquema para crear un nuevo sensor (POST)."""

    pass


class SensorUpdate(BaseModel):
    """Esquema para actualización parcial de un sensor (PATCH)."""

    name: str | None = None
    type: str | None = None
    unit: str | None = None
    min_value: float | None = None
    max_value: float | None = None


class SensorResponse(SensorBase):
    """Esquema de respuesta al cliente (GET / Response)."""

    id: int

    model_config = ConfigDict(from_attributes=True)