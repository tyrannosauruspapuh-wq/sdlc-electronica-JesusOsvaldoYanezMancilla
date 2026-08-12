from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 1. Importar el middleware

from app.routers import reading_router, sensor_router

app = FastAPI(
    title="SensorHub API",
    version="0.1.0",
)

# 2. Permitir peticiones desde cualquier origen (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de los routers por módulo
app.include_router(sensor_router)
app.include_router(reading_router)


@app.get("/", tags=["Health"])
def root() -> dict[str, str]:
    return {"message": "SensorHub API activa", "docs": "/docs"}


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "ok"}