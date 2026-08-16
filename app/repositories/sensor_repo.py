from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.m_sensor import SensorModel
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    """Repositorio para manejar operaciones de base de datos relacionadas
      con Sensores."""

    # Campos permitidos para actualización (whitelist de seguridad)
    ALLOWED_UPDATE_FIELDS = {"name", "type", "unit", "min_value", "max_value"}
    MAX_LIMIT = 1000
    DEFAULT_LIMIT = 20

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self, limit: int | None = None, offset: int = 0) -> list[SensorModel]:
        """Obtiene una lista de sensores con paginación.
        
        Args:
            limit: Cantidad máxima de registros (default: 20, máximo: 1000)
            offset: Número de registros a saltar (debe ser >= 0)
            
        Raises:
            ValueError: Si limit o offset son inválidos
        """
        if limit is None:
            limit = self.DEFAULT_LIMIT
            
        if limit <= 0 or limit > self.MAX_LIMIT:
            raise ValueError(f"limit debe estar entre 1 y {self.MAX_LIMIT}")
        if offset < 0:
            raise ValueError("offset debe ser >= 0")
            
        query = select(SensorModel).offset(offset).limit(limit)
        results: Sequence[SensorModel] = self.session.execute(query).scalars().all()
        return list(results)

    def get_by_id(self, sensor_id: int) -> SensorModel | None:
        """Busca un sensor por su ID único.
        
        Args:
            sensor_id: ID del sensor (debe ser > 0)
            
        Raises:
            ValueError: Si sensor_id es inválido
        """
        if sensor_id <= 0:
            raise ValueError("sensor_id debe ser un entero positivo")
        return self.session.get(SensorModel, sensor_id)

    def create(self, sensor_data: SensorCreate) -> SensorModel:
        """Crea un nuevo sensor en la base de datos.
        
        Raises:
            ValueError: Si hay violación de constraint (ej: duplicado)
            Exception: Para otros errores de base de datos
        """
        try:
            db_sensor = SensorModel(**sensor_data.model_dump())
            self.session.add(db_sensor)
            self.session.commit()
            self.session.refresh(db_sensor)
            return db_sensor
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Violación de constraint en base de datos: {str(e)}") from e  # noqa: E501
        except Exception:
            self.session.rollback()
            raise

    def update(self, sensor_id: int, sensor_data: SensorUpdate) -> SensorModel | None:
        """Actualiza la información de un sensor existente.
        
        Solo permite actualizar campos en ALLOWED_UPDATE_FIELDS por seguridad.
        
        Raises:
            ValueError: Si sensor_id es inválido o se intenta actualizar 
            campo no permitido
            Exception: Para errores de base de datos
        """
        if sensor_id <= 0:
            raise ValueError("sensor_id debe ser un entero positivo")
            
        db_sensor = self.get_by_id(sensor_id)
        if not db_sensor:
            return None

        update_dict = sensor_data.model_dump(exclude_unset=True)
        
        # Validar que solo se actualicen campos permitidos
        for key in update_dict.keys():
            if key not in self.ALLOWED_UPDATE_FIELDS:
                raise ValueError(f"Campo '{key}' no puede ser actualizado")
        
        try:
            for key, value in update_dict.items():
                setattr(db_sensor, key, value)
            self.session.commit()
            self.session.refresh(db_sensor)
            return db_sensor
        except IntegrityError as e:
            self.session.rollback()
            raise ValueError(f"Violación de constraint en base de datos: {str(e)}") from e  # noqa: E501
        except Exception:
            self.session.rollback()
            raise

    def delete(self, sensor_id: int) -> bool:
        """Elimina un sensor de la base de datos.

        Args:
            sensor_id: ID del sensor a eliminar (debe ser > 0)

        Returns:
            True si se eliminó, False si no existe

        Raises:
            ValueError: Si sensor_id es inválido
        """
        if sensor_id <= 0:
            raise ValueError("sensor_id debe ser un entero positivo")

        try:
            # Usar bulk delete para mejor rendimiento (una sola query)
            result = self.session.execute(
                delete(SensorModel).where(SensorModel.id == sensor_id)
            )
            self.session.commit()
            return bool(result.rowcount > 0)  # type: ignore[attr-defined]
        except Exception:
            self.session.rollback()
            raise