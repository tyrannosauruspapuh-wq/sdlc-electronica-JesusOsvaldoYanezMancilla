from sqlalchemy.orm import Session

from app.models.m_sensor import SensorModel
from app.repositories.sensor_repo import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorService:
    """Servicio que coordina la lógica de negocio para Sensores."""

    def __init__(self, db: Session) -> None:
        self.repo = SensorRepository(session=db)

    def create_sensor(self, sensor_data: SensorCreate) -> SensorModel:
        """Crea un nuevo sensor."""
        return self.repo.create(sensor_data)

    def get_sensors(self, limit: int = 50, offset: int = 0) -> list[SensorModel]:
        """Obtiene la lista de sensores paginada."""
        return self.repo.get_all(limit=limit, offset=offset)

    def get_sensor_by_id(self, sensor_id: int) -> SensorModel | None:
        """Obtiene un sensor por su ID."""
        return self.repo.get_by_id(sensor_id)

    def update_sensor(
        self, sensor_id: int, sensor_data: SensorUpdate
    ) -> SensorModel | None:
        """Actualiza la configuración o límites de un sensor."""
        return self.repo.update(sensor_id, sensor_data)

    def delete_sensor(self, sensor_id: int) -> bool:
        """Elimina un sensor."""
        return self.repo.delete(sensor_id)