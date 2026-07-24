import pytest

from semana2.sensor_registry import (
    SensorAlreadyExistsError,  # Se lanzará cuando esté duplicado
    SensorNotFoundError,
    SensorRegistry,
)


def test_get_unknown_sensor_raises_not_found() -> None:
    """US-01: Buscar un sensor inexistente debe lanzar SensorNotFoundError."""
    registry = SensorRegistry()

    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")

def test_register_duplicate_sensor_raises_error() -> None:
    """US-01: Intentar registrar un sensor con ID existente
      debe lanzar SensorAlreadyExistsError."""
    registry = SensorRegistry()
    registry.register("TEMP-01", "Sensor Original")

    # Intentar registrar el mismo ID debe fallar
    with pytest.raises(SensorAlreadyExistsError):
        registry.register("TEMP-01", "Sensor Duplicado")