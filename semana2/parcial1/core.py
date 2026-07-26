from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto


class SensorType(Enum):
    """Tipos de sensores soportados por el sistema."""

    TEMPERATURE = auto()
    HUMIDITY = auto()


@dataclass(frozen=True)
class SensorReading:
    """Modelo de lectura de un sensor con validaciones de rango."""

    sensor_id: str
    value: float
    sensor_type: SensorType
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        """Valida que los valores recibidos sean físicamente coherentes."""
        if self.sensor_type == SensorType.TEMPERATURE:
            if not (-50.0 <= self.value <= 100.0):
                raise ValueError(
                    f"Temperatura fuera de rango (-50 a 100 °C): {self.value}"
                )
        elif self.sensor_type == SensorType.HUMIDITY:
            if not (0.0 <= self.value <= 100.0):
                raise ValueError(
                    f"Humedad fuera de rango (0 a 100%): {self.value}"
                )


class AnomalyDetector:
    """Detector de anomalías con umbrales configurables (inyectados)."""

    def __init__(self, max_temp: float = 35.0, max_humidity: float = 80.0) -> None:
        self.max_temp = max_temp
        self.max_humidity = max_humidity

    def is_anomaly(self, reading: SensorReading) -> bool:
        """Determina si una lectura supera los umbrales configurados."""
        if reading.sensor_type == SensorType.TEMPERATURE:
            return reading.value > self.max_temp
        if reading.sensor_type == SensorType.HUMIDITY:
            return reading.value > self.max_humidity
        return False


class AlertStrategy(ABC):
    """Interfaz abstracta para la emisión de alertas (Patrón Estrategia)."""

    @abstractmethod
    def send(self, message: str) -> None:
        """Envía el mensaje de alerta según la implementación concreta."""
        pass


class ConsoleAlert(AlertStrategy):
    """Estrategia de alerta por consola estándar."""

    def send(self, message: str) -> None:
        print(f"[ALERTA CONSOLA] {message}")


class FileAlert(AlertStrategy):
    """Estrategia de alerta guardada en archivo de log."""

    def __init__(self, filepath: str = "alerts.log") -> None:
        self.filepath = filepath

    def send(self, message: str) -> None:
        now = datetime.now().isoformat()
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"[{now}] [ALERTA] {message}\n")


class AlertManager:
    """Coordinador multicanal para la emisión de alertas."""

    def __init__(self) -> None:
        self._strategies: list[AlertStrategy] = []

    def add_strategy(self, strategy: AlertStrategy) -> None:
        """Agrega una nueva estrategia de emisión."""
        self._strategies.append(strategy)

    def notify(self, reading: SensorReading, reason: str) -> None:
        """Notifica la anomalía a todas las estrategias registradas."""
        message = f"[{reading.sensor_id}] {reason}"
        for strategy in self._strategies:
            strategy.send(message)