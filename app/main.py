from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

# Importa tus componentes de los archivos correspondientes
from app.db import Base, engine, get_db
from app.schemas.reading import SensorReadingIn, SensorReadingOut

app = FastAPI(title="SensorHub API", version="0.1.0")

# Crea las tablas en la base de datos (SQLite) al iniciar la app
# En la semana 4/5 esto lo manejará Alembic con migraciones
Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/readings", response_model=SensorReadingOut, status_code=201)
def create_reading(
    reading: SensorReadingIn, db: Session = Depends(get_db)
) -> SensorReadingOut:
    # Mañana (Miércoles - Día 4) implementas la persistencia real en `db`
    # Por hoy retornas el mock con ID
    return SensorReadingOut(id=1, **reading.model_dump())