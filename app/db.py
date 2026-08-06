import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# Función sugerida por la guía para normalizar la URL de la base de datos
def get_database_url() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///./sensorhub.db")
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg://", 1)
    if url.startswith("postgresql://") and "+psycopg" not in url:
        return url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url

# Obtenemos la URL ya normalizada
DATABASE_URL = get_database_url()

# connect_args solo es necesario si la base de datos es SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Creamos el engine con la URL resultante
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para todos los modelos ORM (SQLAlchemy 2.x)
class Base(DeclarativeBase):
    pass

# Generador para inyección de dependencias en FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()