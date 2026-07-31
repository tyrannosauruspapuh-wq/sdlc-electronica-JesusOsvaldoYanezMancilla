from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models.reading import ReadingModel
from app.schemas.reading import SensorReadingIn, SensorReadingOut, SensorReadingUpdate

app = FastAPI(title="SensorHub API", version="0.1.0")

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# 1. CREAR LECTURA PARA UN SENSOR -> POST /sensors/{sensor_id}/readings
@app.post(
    "/sensors/{sensor_id}/readings",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_sensor_reading(
    sensor_id: str,
    reading: SensorReadingIn,
    db: Session = Depends(get_db),
) -> ReadingModel:
    db_reading = ReadingModel(
        sensor_id=sensor_id,
        value=reading.value,
        unit=reading.unit,
    )
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading


# 2. LISTAR LECTURAS DE UN SENSOR (Con Paginación y Filtros de Fechas) -> 
# GET /sensors/{sensor_id}/readings
@app.get(
    "/sensors/{sensor_id}/readings",
    response_model=list[SensorReadingOut],
)
def list_sensor_readings(
    sensor_id: str,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    from_date: Annotated[datetime | None, Query(alias="from")] = None,
    to_date: Annotated[datetime | None, Query(alias="to")] = None,
    db: Session = Depends(get_db),
) -> list[ReadingModel]:
    stmt = select(ReadingModel).where(ReadingModel.sensor_id == sensor_id)

    if from_date:
        stmt = stmt.where(ReadingModel.created_at >= from_date)
    if to_date:
        stmt = stmt.where(ReadingModel.created_at <= to_date)

    stmt = stmt.limit(limit).offset(offset)
    readings = db.scalars(stmt).all()
    return list(readings)


# 3. OBTENER LECTURA POR ID -> GET /readings/{reading_id}
@app.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(
    reading_id: int,
    db: Session = Depends(get_db),
) -> ReadingModel:
    stmt = select(ReadingModel).where(ReadingModel.id == reading_id)
    reading = db.scalar(stmt)

    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con id {reading_id} no encontrada",
        )
    return reading


# 4. ACTUALIZAR PARCIALMENTE -> PATCH /readings/{reading_id}
@app.patch("/readings/{reading_id}", response_model=SensorReadingOut)
def update_reading(
    reading_id: int,
    reading_update: SensorReadingUpdate,
    db: Session = Depends(get_db),
) -> ReadingModel:
    stmt = select(ReadingModel).where(ReadingModel.id == reading_id)
    db_reading = db.scalar(stmt)

    if not db_reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con id {reading_id} no encontrada para actualizar",
        )

    # Actualiza únicamente los campos que envió el cliente
    update_data = reading_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reading, field, value)

    db.commit()
    db.refresh(db_reading)
    return db_reading


# 5. ELIMINAR LECTURA -> DELETE /readings/{reading_id} (204 No Content)
@app.delete(
    "/readings/{reading_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_reading(
    reading_id: int,
    db: Session = Depends(get_db),
) -> Response:
    stmt = select(ReadingModel).where(ReadingModel.id == reading_id)
    db_reading = db.scalar(stmt)

    if not db_reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con id {reading_id} no encontrada para eliminar",
        )

    db.delete(db_reading)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)