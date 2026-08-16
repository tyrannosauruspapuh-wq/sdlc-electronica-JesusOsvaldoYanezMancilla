from sqlalchemy import CheckConstraint, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.db import Base


class SensorModel(Base):
    __tablename__ = "sensors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)
    min_value: Mapped[float] = mapped_column(Float, nullable=False)
    max_value: Mapped[float] = mapped_column(Float, nullable=False)

    __table_args__ = (
        CheckConstraint("min_value <= max_value", name="check_min_max_range"),
    )

    # Relación con carga optimizada (evita N+1 queries)
    readings = relationship(
        "ReadingModel",
        back_populates="sensor",
        cascade="save-update, merge",
        lazy="selectin",
    )

    @validates("name", "type", "unit")
    def validate_non_empty_strings(self, key: str, value: str) -> str:
        """Valida que strings no sean vacíos y elimina espacios."""
        if not value or not value.strip():
            raise ValueError(f"{key} no puede estar vacío")
        return value.strip()

    @validates("min_value", "max_value")
    def validate_range_values(self, key: str, value: float) -> float:
        """Valida que min_value <= max_value asegurando que ninguno sea None al 
        instanciar."""
        if value is None:
            raise ValueError(f"{key} no puede ser None")

        # Obtenemos los valores actuales de forma segura
        current_min = value if key == "min_value" else getattr(self, "min_value", None)
        current_max = value if key == "max_value" else getattr(self, "max_value", None)

        # Solo comparamos si AMBOS ya fueron asignados y no son None
        if current_min is not None and current_max is not None:
            if current_min > current_max:
                raise ValueError(
                    f"min_value ({current_min}) no puede ser mayor que max_value ({current_max})"  # noqa: E501
                )

        return value