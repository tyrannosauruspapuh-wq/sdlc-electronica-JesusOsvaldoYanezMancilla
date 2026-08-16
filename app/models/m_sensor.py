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
        CheckConstraint('min_value <= max_value', name='check_min_max_range'),
    )

    # Relación con carga optimizada (evita N+1 queries)
    readings = relationship(
        "ReadingModel",
        back_populates="sensor",
        cascade="save-update, merge",
        lazy="selectin",
    )

    @validates('name', 'type', 'unit')
    def validate_non_empty_strings(self, key: str, value: str) -> str:
        """Valida que strings no sean vacíos y elimina espacios"""
        if not value or not value.strip():
            raise ValueError(f"{key} no puede estar vacío")
        return value.strip()

    @validates('min_value', 'max_value')
    def validate_range_values(self, key: str, value: float) -> float:
        """Valida que min_value <= max_value"""
        if value is None:
            raise ValueError(f"{key} no puede ser None")
        if hasattr(self, 'min_value') and hasattr(self, 'max_value'):
            min_val = self.min_value if key == 'max_value' else value
            max_val = self.max_value if key == 'min_value' else value
            if min_val > max_val:
                raise ValueError
            (f"min_value ({min_val}) no puede ser mayor que max_value ({max_val})")
        return value