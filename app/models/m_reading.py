from datetime import UTC, datetime
from math import isfinite

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import Base


class ReadingModel(Base):
    __tablename__ = "readings"
    __table_args__ = (
        Index("ix_readings_sensor_created_at", "sensor_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    sensor_id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(16), default="C", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    # Relación bidireccional con el modelo Sensor
    sensor = relationship("SensorModel", back_populates="readings")

    @validates("value")
    def validate_value(self, key: str, value: float) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("El valor de la lectura debe ser numérico.")
        if not isfinite(float(value)):
            raise ValueError("El valor de la lectura no puede ser NaN ni infinito.")
        return float(value)

    @validates("unit")
    def validate_unit(self, key: str, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("La unidad debe ser un texto.")
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("La unidad no puede estar vacía.")
        if len(cleaned) > 16:
            raise ValueError("La unidad es demasiado larga.")
        return cleaned