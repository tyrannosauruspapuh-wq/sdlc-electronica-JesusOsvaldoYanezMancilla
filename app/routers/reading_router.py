from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.m_reading import ReadingModel
from app.schemas.reading import ReadingCreate, ReadingResponse
from app.services.reading_service import ReadingService

router = APIRouter(tags=["Readings"])


def get_reading_service(db: Session = Depends(get_db)) -> ReadingService:
    return ReadingService(db=db)


@router.post(
    "/sensors/{sensor_id}/readings",
    response_model=ReadingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nueva lectura para un sensor",
)
def create_reading(
    sensor_id: int,
    reading_data: ReadingCreate,
    service: ReadingService = Depends(get_reading_service),
) -> ReadingModel:
    reading_data.sensor_id = sensor_id
    try:
        return service.record_reading(reading_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[ReadingResponse],
    summary="Listar lecturas registradas para un sensor",
)
def list_readings_by_sensor(
    sensor_id: int,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    from_date: Annotated[datetime | None, Query(alias="from")] = None,
    to_date: Annotated[datetime | None, Query(alias="to")] = None,
    service: ReadingService = Depends(get_reading_service),
) -> list[ReadingModel]:
    return service.get_readings_by_sensor(
        sensor_id=sensor_id,
        limit=limit,
        offset=offset,
        from_date=from_date,
        to_date=to_date,
    )


@router.get(
    "/readings/{reading_id}",
    response_model=ReadingResponse,
    summary="Obtener lectura por su ID único",
)
def get_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
) -> ReadingModel:
    reading = service.get_reading_by_id(reading_id)
    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con id {reading_id} no encontrada",
        )
    return reading


@router.delete(
    "/readings/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una lectura",
)
def delete_reading(
    reading_id: int,
    service: ReadingService = Depends(get_reading_service),
) -> Response:
    deleted = service.delete_reading(reading_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con id {reading_id} no encontrada para eliminar",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)