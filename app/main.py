from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.models.reading import ReadingModel
from app.schemas.reading import SensorReadingIn, SensorReadingOut

app = FastAPI(title="SensorHub API", version="0.1.0")

# Crea las tablas al iniciar la app
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# CREAR (POST) -> Guarda en SQLite
@app.post(
    "/readings",
    response_model=SensorReadingOut,
    status_code=status.HTTP_201_CREATED,
)
def create_reading(
    reading: SensorReadingIn, db: Session = Depends(get_db)
) -> ReadingModel:
    # 1. Instanciamos el modelo ORM con los datos que llegaron
    db_reading = ReadingModel(**reading.model_dump())

    # 2. Operaciones de sesión de SQLAlchemy
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)  # Asigna el ID autogenerado y el timestamp

    return db_reading


# LISTAR (GET) -> Consulta desde SQLite
@app.get("/readings", response_model=list[SensorReadingOut])
def list_readings(db: Session = Depends(get_db)) -> list[ReadingModel]:
    # Consulta usando la sintaxis moderna de SQLAlchemy 2.x
    stmt = select(ReadingModel)
    readings = db.scalars(stmt).all()
    return list(readings)


# OBTENER POR ID (GET /readings/{reading_id})
@app.get("/readings/{reading_id}", response_model=SensorReadingOut)
def get_reading(
    reading_id: int, db: Session = Depends(get_db)
) -> ReadingModel:
    stmt = select(ReadingModel).where(ReadingModel.id == reading_id)
    reading = db.scalar(stmt)

    if not reading:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Lectura con id {reading_id} no encontrada",
        )

    return reading