from fastapi import status
from fastapi.testclient import TestClient


def test_create_sensor(client: TestClient) -> None:
    """Prueba la creación exitosa de un sensor (201 Created)."""
    payload = {
        "name": "Sensor de Temperatura Lab 1",
        "type": "temperature",
        "unit": "C",
        "min_value": -50.0,
        "max_value": 100.0,
    }
    response = client.post("/sensors", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == payload["name"]
    assert "id" in data


def test_get_sensor_by_id(client: TestClient) -> None:
    """Prueba la obtención de un sensor existente (200 OK) 
    y no existente (404 Not Found)."""
    # 1. Crear sensor
    payload = {
        "name": "Sensor Presión",
        "type": "pressure",
        "unit": "Pa",
        "min_value": 0.0,
        "max_value": 5000.0,
    }
    created = client.post("/sensors", json=payload).json()
    sensor_id = created["id"]

    # 2. Consultar id existente
    response = client.get(f"/sensors/{sensor_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == sensor_id

    # 3. Consultar id inexistente
    response_404 = client.get("/sensors/99999")
    assert response_404.status_code == status.HTTP_404_NOT_FOUND


def test_list_sensors_pagination(client: TestClient) -> None:
    """Prueba la lista paginada de sensores."""
    for i in range(3):
        client.post(
            "/sensors",
            json={
                "name": f"Sensor {i}",
                "type": "temp",
                "unit": "C",
                "min_value": 0.0,
                "max_value": 100.0,
            },
        )

    response = client.get("/sensors?limit=2&offset=0")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2