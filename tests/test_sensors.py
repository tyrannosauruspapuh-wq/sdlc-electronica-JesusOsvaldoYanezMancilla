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
    """Prueba la obtención de un sensor existente (200 OK) y no existente
      (404 Not Found)."""
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


def test_create_sensor_invalid_range(client: TestClient) -> None:
    """Prueba que no se permita crear un sensor con min_value > max_value."""
    payload = {
        "name": "Sensor Invalido",
        "type": "temperature",
        "unit": "C",
        "min_value": 50.0,
        "max_value": 10.0,
    }
    response = client.post("/sensors", json=payload)
    assert response.status_code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def test_list_sensors_invalid_limit(client: TestClient) -> None:
    """Prueba que límites de paginación negativos o excesivos sean rechazados."""
    response_neg = client.get("/sensors?limit=-5")
    assert response_neg.status_code in (
        status.HTTP_400_BAD_REQUEST,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def test_get_sensor_negative_id(client: TestClient) -> None:
    """Prueba que la consulta con IDs negativos o cero retorne error."""
    response = client.get("/sensors/-1")
    assert response.status_code in (
        status.HTTP_404_NOT_FOUND,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def test_update_sensor_success_and_fail(client: TestClient) -> None:
    """Prueba la actualización parcial (PATCH) de un sensor existente y no existente."""
    # 1. Crear sensor
    payload = {
        "name": "Sensor Nivel de Agua",
        "type": "level",
        "unit": "m",
        "min_value": 0.0,
        "max_value": 20.0,
    }
    sensor = client.post("/sensors", json=payload).json()
    sensor_id = sensor["id"]

    # 2. Actualizar parcialmente campo 'name'
    patch_res = client.patch(f"/sensors/{sensor_id}", json={"name": "Sensor Tanque Principal"})  # noqa: E501
    assert patch_res.status_code == status.HTTP_200_OK
    assert patch_res.json()["name"] == "Sensor Tanque Principal"

    # 3. Intentar actualizar sensor que no existe
    patch_fail = client.patch("/sensors/99999", json={"name": "Fantasma"})
    assert patch_fail.status_code == status.HTTP_404_NOT_FOUND


def test_delete_sensor_success_and_fail(client: TestClient) -> None:
    """Prueba la eliminación (DELETE) de un sensor existente y no existente."""
    # 1. Crear sensor
    payload = {
        "name": "Sensor Volátil",
        "type": "gas",
        "unit": "ppm",
        "min_value": 0.0,
        "max_value": 1000.0,
    }
    sensor = client.post("/sensors", json=payload).json()
    sensor_id = sensor["id"]

    # 2. Eliminar (204 No Content)
    del_res = client.delete(f"/sensors/{sensor_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT

    # 3. Eliminar de nuevo (404 Not Found)
    del_fail = client.delete(f"/sensors/{sensor_id}")
    assert del_fail.status_code == status.HTTP_404_NOT_FOUND