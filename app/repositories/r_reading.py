from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.m_reading import ReadingModel
from app.schemas.reading import ReadingCreate


class ReadingRepository:
    """Repositorio para manejar operaciones de base de datos relacionadas con Lecturas."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, reading_data: ReadingCreate) -> ReadingModel:
        """Guarda una nueva lectura asociada a un sensor."""
        db_reading = ReadingModel(**reading_data.model_dump())
        self.session.add(db_reading)
        self.session.commit()
        self.session.refresh(db_reading)
        return db_reading

    def get_by_id(self, reading_id: int) -> ReadingModel | None:
        """Busca una lectura específica por su ID."""
        return self.session.get(ReadingModel, reading_id)

    def get_by_sensor(
        self, sensor_id: int, limit: int = 50, offset: int = 0
    ) -> list[ReadingModel]:
        """Obtiene todas las lecturas registradas para un sensor en particular."""
        query = (
            select(ReadingModel)
            .where(ReadingModel.sensor_id == sensor_id)
            .offset(offset)
            .limit(limit)
        )
        results: Sequence[ReadingModel] = self.session.execute(query).scalars().all()
        return list(results)

    def delete(self, reading_id: int) -> bool:
        """Elimina una lectura por su ID."""
        db_reading = self.get_by_id(reading_id)
        if not db_reading:
            return False

        self.session.delete(db_reading)
        self.session.commit()
        return True