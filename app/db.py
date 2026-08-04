from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Crea una base de datos local SQLite en la raíz
DATABASE_URL = "sqlite:///./sensorhub.db"

# connect_args solo es necesario para SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Clase base para todos nuestros modelos ORM (SQLAlchemy 2.x)
class Base(DeclarativeBase):
    pass


# Generador para inyección de dependencias en FastAPI
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()