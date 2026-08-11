from fastapi import FastAPI

from app.routers import reading_router, sensor_router

app = FastAPI(
    title="SensorHub API",
    version="0.1.0",
)

# Registro de los routers por módulo
app.include_router(sensor_router)
app.include_router(reading_router)


@app.get("/health", tags=["Health"])
def health() -> dict[str, str]:
    return {"status": "ok"}