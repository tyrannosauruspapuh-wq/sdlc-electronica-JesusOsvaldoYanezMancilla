from datetime import datetime

import pytest
from semana2.eval1.core import (
    AlertManager,
    AnomalyDetector,
    ConsoleAlert,
    FileAlert,
    SensorReading,
    SensorType,
)


# --- Tests para SensorReading ---
def test_sensor_reading_creation_valid() -> None:
    now = datetime.now()
    reading = SensorReading(
        sensor_id="TEMP-01",
        value=25.5,
        sensor_type=SensorType.TEMPERATURE,
        timestamp=now,
    )
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 25.5
    assert reading.sensor_type == SensorType.TEMPERATURE
    assert reading.timestamp == now


def test_sensor_reading_invalid_temperature_low() -> None:
    with pytest.raises(ValueError, match="Temperatura fuera de rango"):
        SensorReading(
            sensor_id="TEMP-01",
            value=-60.0,
            sensor_type=SensorType.TEMPERATURE,
        )


def test_sensor_reading_invalid_humidity() -> None:
    with pytest.raises(ValueError, match="Humedad fuera de rango"):
        SensorReading(
            sensor_id="HUM-01",
            value=105.0,
            sensor_type=SensorType.HUMIDITY,
        )


# --- Tests para AnomalyDetector ---
def test_anomaly_detector_temperature_anomaly() -> None:
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)
    reading = SensorReading(
        sensor_id="TEMP-01",
        value=38.5,
        sensor_type=SensorType.TEMPERATURE,
    )
    assert detector.is_anomaly(reading) is True


def test_anomaly_detector_temperature_normal() -> None:
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)
    reading = SensorReading(
        sensor_id="TEMP-01",
        value=22.0,
        sensor_type=SensorType.TEMPERATURE,
    )
    assert detector.is_anomaly(reading) is False


def test_anomaly_detector_humidity_anomaly() -> None:
    detector = AnomalyDetector(max_temp=35.0, max_humidity=80.0)
    reading = SensorReading(
        sensor_id="HUM-01",
        value=85.0,
        sensor_type=SensorType.HUMIDITY,
    )
    assert detector.is_anomaly(reading) is True


# --- Tests para AlertManager y Estrategias ---
def test_console_alert_emits_message(capsys: pytest.CaptureFixture[str]) -> None:
    alert_strategy = ConsoleAlert()
    alert_strategy.send("Alerta de prueba")
    captured = capsys.readouterr()
    assert "[ALERTA CONSOLA] Alerta de prueba" in captured.out


def test_file_alert_writes_to_file(tmp_path: pytest.TempPathFactory) -> None:
    log_file = tmp_path / "test_alerts.log"  # type: ignore[operator]
    file_alert = FileAlert(filepath=str(log_file))
    file_alert.send("Anomalía detectada en TEMP-01")

    content = log_file.read_text(encoding="utf-8")
    assert "Anomalía detectada en TEMP-01" in content


def test_alert_manager_notifies_all_strategies(capsys: pytest.CaptureFixture[str], 
tmp_path: pytest.TempPathFactory) -> None:
    log_file = tmp_path / "test_alerts.log"  # type: ignore[operator]
    console_strategy = ConsoleAlert()
    file_strategy = FileAlert(filepath=str(log_file))

    manager = AlertManager()
    manager.add_strategy(console_strategy)
    manager.add_strategy(file_strategy)

    reading = SensorReading(
        sensor_id="TEMP-01",
        value=40.0,
        sensor_type=SensorType.TEMPERATURE,
    )
    manager.notify(reading, "Temperatura crítica alcanzada")

    captured = capsys.readouterr()
    assert "[ALERTA CONSOLA] [TEMP-01] Temperatura crítica alcanzada" in captured.out

    content = log_file.read_text(encoding="utf-8")
    assert "[TEMP-01] Temperatura crítica alcanzada" in content