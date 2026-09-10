from collections.abc import Sequence
from datetime import datetime
from typing import cast

from sqlalchemy import delete as sql_delete
from sqlalchemy import select
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.m_reading import ReadingModel
from app.schemas.reading import ReadingCreate


class ReadingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, reading_data: ReadingCreate) -> ReadingModel:
        try:
            db_reading = ReadingModel(**reading_data.model_dump())
            self.session.add(db_reading)
            self.session.commit()
            self.session.flush()  # Ensure ID is assigned without extra query
            return db_reading
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError("Lectura duplicada o datos inválidos") from e

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        return self.session.get(ReadingModel, reading_id)

    def get_by_sensor(
        self,
        sensor_id: int,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:
        # Validar parámetros
        if sensor_id <= 0:
            raise ValueError("sensor_id debe ser positivo")
        if limit < 0:
            raise ValueError("limit no puede ser negativo")
        if offset < 0:
            raise ValueError("offset no puede ser negativo")
        if from_date and to_date and from_date > to_date:
            raise ValueError("from_date debe ser menor o igual a to_date")

        query = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)

        # Filtros opcionales de rango de fechas
        if from_date:
            query = query.where(ReadingModel.created_at >= from_date)
        if to_date:
            query = query.where(ReadingModel.created_at <= to_date)

        query = query.offset(offset).limit(limit)
        results: Sequence[ReadingModel] = self.session.execute(query).scalars().all()
        return list(results)

    def delete(self, reading_id: int) -> bool:
        """Delete a reading by ID. Uses direct DELETE query for better performance."""
        if reading_id <= 0:
            raise ValueError("reading_id debe ser positivo")

        try:
            stmt = sql_delete(ReadingModel).where(ReadingModel.id == reading_id)
            result = cast(CursorResult, self.session.execute(stmt))
            self.session.commit()
            return bool(result.rowcount > 0)
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError("No se puede eliminar: hay referencias a esta lectura") from e  # noqa: E501
