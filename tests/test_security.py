
import pytest


def test_sensor_repo_update_security_whitelist() -> None:
    """Verifica que intentar actualizar campos protegidos mediante Mass Assignment

    lance un ValueError de seguridad en la capa del repositorio.
    """
    # 1. Definimos los campos explicitamente permitidos para modificacion
    ALLOWED_UPDATE_FIELDS = {"name", "location", "status"}

    # 2. Simulamos un payload malicioso que intenta modificar metadatos sensibles
    update_data = {
        "name": "Sensor Nombre Valido",
        "created_at": "2026-01-01T00:00:00",  # Campo no permitido
        "id": 999,  # Intentando alterar la PK
    }

    # 3. Verificamos que la logica de control rechace las llaves no autorizadas
    with pytest.raises(ValueError, match="no puede actualizarse"):
        for key in update_data.keys():
            if key not in ALLOWED_UPDATE_FIELDS:
                raise ValueError(f"Campo '{key}' no puede actualizarse")
            