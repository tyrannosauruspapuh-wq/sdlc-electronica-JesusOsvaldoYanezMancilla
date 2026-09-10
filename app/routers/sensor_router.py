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
    try:
        return service.create_sensor(sensor_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "",
    response_model=list[SensorResponse],
    summary="Listar todos los sensores con paginación",
)
def list_sensors(
    limit: Annotated[int, Query(ge=1, le=1000)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    service: SensorService = Depends(get_sensor_service),
) -> list[SensorModel]:
    try:
        return service.get_sensors(limit=limit, offset=offset)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/{sensor_id}",
    response_model=SensorResponse,
    summary="Obtener un sensor por ID",
)
def get_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> SensorModel:
    try:
        sensor = service.get_sensor_by_id(sensor_id)
    except ValueError:
        # Si el repositorio lanza ValueError por ID negativo, respondemos 404
        raise HTTPException(  # noqa: B904
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con id {sensor_id} no encontrado",
        )

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
    try:
        sensor = service.update_sensor(sensor_id, sensor_data)
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor con id {sensor_id} no encontrado para actualizar",
            )
        return sensor
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete(
    "/{sensor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un sensor",
)
def delete_sensor(
    sensor_id: int,
    service: SensorService = Depends(get_sensor_service),
) -> Response:
    try:
        deleted = service.delete_sensor(sensor_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor con id {sensor_id} no encontrado para eliminar",
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e