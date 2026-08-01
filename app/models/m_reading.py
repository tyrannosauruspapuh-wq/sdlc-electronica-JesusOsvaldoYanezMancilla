from datetime import UTC, datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class ReadingModel(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sensor_id: Mapped[str] = mapped_column(String, index=True)
    value: Mapped[float]
    unit: Mapped[str] = mapped_column(String, default="C")
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(UTC)
    )