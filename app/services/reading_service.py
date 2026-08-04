from datetime import datetime

from sqlalchemy.orm import Session

from app.models.m_reading import ReadingModel
from app.repositories.reading_repo import ReadingRepository
from app.repositories.sensor_repo import SensorRepository
from app.schemas.reading import ReadingCreate


class ReadingService:
    def __init__(self, db: Session) -> None:
        self.reading_repo = ReadingRepository(session=db)
        self.sensor_repo = SensorRepository(session=db)

    def record_reading(self, reading_data: ReadingCreate) -> ReadingModel:
        sensor = self.sensor_repo.get_by_id(reading_data.sensor_id)
        if not sensor:
            raise ValueError(
                f"No existe un sensor registrado con id {reading_data.sensor_id}"
            )

        is_below_min = reading_data.value < sensor.min_value
        is_above_max = reading_data.value > sensor.max_value

        if is_below_min or is_above_max:
            msg = (
                f"El valor {reading_data.value} esta fuera del rango "
                f"permitido [{sensor.min_value}, {sensor.max_value}] "
                f"para el sensor '{sensor.name}'"
            )
            raise ValueError(msg)

        return self.reading_repo.create(reading_data)

    def get_readings_by_sensor(
        self,
        sensor_id: int,
        limit: int = 50,
        offset: int = 0,
        from_date: datetime | None = None,
        to_date: datetime | None = None,
    ) -> list[ReadingModel]:
        return self.reading_repo.get_by_sensor(
            sensor_id=sensor_id,
            limit=limit,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )

    def get_reading_by_id(self, reading_id: int) -> ReadingModel | None:
        return self.reading_repo.get_by_id(reading_id)

    def delete_reading(self, reading_id: int) -> bool:
        return self.reading_repo.delete(reading_id)