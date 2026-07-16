# Autor: Jesús Osvaldo Yáñez Mancilla
# Fecha 15/07/26
# Primer código para la semana 1, busca implementar 5 funciones de READING usando type hints complejos.

from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol, List

class SensorType(Enum):
    TEMPERATURE = auto()  # Solo dejamos temperatura, limpio de código muerto.

@dataclass(frozen=True)
class Reading:
    """
    Molde inmutable para representar una lectura de sensor.
    Al ser frozen=True, garantizamos que las funciones no alteren los datos.
    """
    sensor_id: str
    value: float
    sensor_type: SensorType

class Transport(Protocol):
    """Interfaz para envío de datos (Duck Typing estático)."""
    def send(self, payload: bytes) -> None: ...


# FUNCIONES PURAS DE CONVERSIÓN
def celsius_to_fahrenheit(temp_c: float) -> float:
    """Convierte un valor numérico de Celsius a Fahrenheit de forma pura."""
    return (temp_c * 9 / 5) + 32


def convert_reading_to_imperial(r: Reading) -> Reading:
    """
    Toma una lectura en Celsius y devuelve una NUEVA lectura en Fahrenheit.
    Es pura: no modifica 'r', genera un objeto Reading completamente nuevo.
    """
    return Reading(
        sensor_id=r.sensor_id,
        value=celsius_to_fahrenheit(r.value),
        sensor_type=r.sensor_type
    )

# FUNCIONES PURAS DE UMBRAL (THRESHOLD)

def is_above_threshold(r: Reading, threshold: float) -> bool:
    """Verifica de forma pura si el valor de la lectura supera un límite."""
    return r.value > threshold


def filter_high_readings(readings: List[Reading], threshold: float) -> List[Reading]:
    """
    Filtra una lista de lecturas y devuelve una lista NUEVA con las que superan el umbral.
    Es pura: no altera la lista original que recibió.
    """
    return [r for r in readings if is_above_threshold(r, threshold)
            
#  FUNCIÓN PURA DE SERIALIZACIÓN
def to_frame(r: Reading) -> bytes:
    """
    Serializa la lectura pasándola a un formato de bytes para transmisión.
    Es pura: el output depende únicamente del input 'r'.
    """
    return f"{r.sensor_id}:{r.value:.2f}".encode()
