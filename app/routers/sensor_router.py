from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.m_sensor import SensorModel
from app.schemas.sensor import SensorCreate, SensorResponse, SensorUpdate
from app.services.sensor_service import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


def get_sensor_service(db: Session = Depends(get_db)) -> SensorService:
    return SensorService(db=db)


@router.post(
    "",
    response_model=SensorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo sensor",
)
def create_sensor(
    sensor_data: SensorCreate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:
    return service.create_sensor(sensor_data)


@router.get(
    "",
    response_model=list[SensorResponse],
    summary="Listar todos los sensores con paginación",
)
def list_sensors(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorModel]:
    return service.get_sensors(limit=limit, offset=offset)


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
    summary="Obtener un sensor por ID",
)
def get_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:
    sensor = service.get_sensor_by_id(sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con id {sensor_id} no encontrado",
        )
    return sensor


@router.patch(
    "/{sensor_id}",
    response_model=SensorResponse,
    summary="Actualizar parcialmente un sensor",
)
def update_sensor(
    sensor_id: int,
    sensor_data: SensorUpdate,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:
    sensor = service.update_sensor(sensor_id, sensor_data)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con id {sensor_id} no encontrado para actualizar",
        )
    return sensor


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un sensor",
)
def delete_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> Response:
    deleted = service.delete_sensor(sensor_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con id {sensor_id} no encontrado para eliminar",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)