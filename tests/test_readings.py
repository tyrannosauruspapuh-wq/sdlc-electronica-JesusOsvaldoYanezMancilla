from fastapi import status
from fastapi.testclient import TestClient


def test_record_reading_success(client: TestClient) -> None:
    """Prueba guardar una lectura dentro del rango válido."""
    # Crear sensor primero
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor Térmico",
            "type": "temperature",
            "unit": "C",
            "min_value": -10.0,
            "max_value": 50.0,
        },
    ).json()

    sensor_id = sensor["id"]

    # Registrar lectura válida
    payload = {"value": 22.5, "unit": "C", "sensor_id": sensor_id}
    response = client.post(f"/sensors/{sensor_id}/readings", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["value"] == 22.5
    assert data["sensor_id"] == sensor_id


def test_record_reading_out_of_range(client: TestClient) -> None:
    """Prueba que se rechace (400 Bad Request) una lectura fuera de 
    los rangos físicos."""
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor Térmico Estricto",
            "type": "temperature",
            "unit": "C",
            "min_value": 0.0,
            "max_value": 30.0,
        },
    ).json()

    sensor_id = sensor["id"]

    # Intentar enviar lectura de 150.0 °C (Límite max: 30.0)
    payload = {"value": 150.0, "unit": "C", "sensor_id": sensor_id}
    response = client.post(f"/sensors/{sensor_id}/readings", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "fuera del rango" in response.json()["detail"]


def test_readings_date_filter(client: TestClient) -> None:
    """Prueba el filtrado por fechas ?from=...&to=..."""
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor Humedad",
            "type": "humidity",
            "unit": "%",
            "min_value": 0.0,
            "max_value": 100.0,
        },
    ).json()
    sensor_id = sensor["id"]

    # Guardar lectura
    client.post(
        f"/sensors/{sensor_id}/readings",
        json={"value": 45.0, "unit": "%", "sensor_id": sensor_id},
    )

    # Filtrar con fecha futura
    response = client.get(
        f"/sensors/{sensor_id}/readings?from=2030-01-01T00:00:00"
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0