import pytest
from semana2.sensor_registry import SensorRegistry, SensorNotFoundError


def test_get_unknown_sensor_raises_not_found():
    """US-01: Buscar un sensor inexistente debe lanzar SensorNotFoundError."""
    registry = SensorRegistry()

    with pytest.raises(SensorNotFoundError):
        registry.get("GHOST-99")
