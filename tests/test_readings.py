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
    """Prueba que se rechace (400 Bad Request) una lectura fuera de los rangos 
    físicos."""
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


def test_readings_invalid_date_range(client: TestClient) -> None:
    """Prueba que un rango con 'from' superior a 'to' devuelva un error 400 Bad
      Request."""
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor Test Fechas",
            "type": "temp",
            "unit": "C",
            "min_value": -10.0,
            "max_value": 50.0,
        },
    ).json()

    response = client.get(
        f"/sensors/{sensor['id']}/readings?from=2026-12-31T00:00:00&to=2026-01-01T00:00:00"
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_reading_by_id_and_delete(client: TestClient) -> None:
    """Prueba la consulta individual de lecturas y su posterior eliminación."""
    # 1. Crear sensor
    sensor = client.post(
        "/sensors",
        json={
            "name": "Sensor Flujo",
            "type": "flow",
            "unit": "L/min",
            "min_value": 0.0,
            "max_value": 500.0,
        },
    ).json()
    sensor_id = sensor["id"]

    # 2. Registrar lectura
    reading = client.post(
        f"/sensors/{sensor_id}/readings",
        json={"value": 120.5, "unit": "L/min", "sensor_id": sensor_id},
    ).json()
    reading_id = reading["id"]

    # 3. Consultar lectura por id (200 OK)
    res_get = client.get(f"/readings/{reading_id}")
    assert res_get.status_code == status.HTTP_200_OK
    assert res_get.json()["id"] == reading_id

    # 4. Eliminar lectura (204 No Content)
    res_del = client.delete(f"/readings/{reading_id}")
    assert res_del.status_code == status.HTTP_204_NO_CONTENT

    # 5. Confirmar que ya no existe (404 Not Found)
    res_404 = client.get(f"/readings/{reading_id}")
    assert res_404.status_code == status.HTTP_404_NOT_FOUND


def test_reading_not_found_deletes(client: TestClient) -> None:
    """Prueba eliminar una lectura inexistente."""
    response = client.delete("/readings/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND