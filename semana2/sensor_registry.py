
##Código de testeo para la semana 2
##Autor: Jesús Osvaldo Yáñez Mancilla
class SensorNotFoundError(Exception):
    """Excepción lanzada cuando un sensor no existe en el registro."""

    pass


class SensorRegistry:
    """Gestor en memoria para el registro de sensores del sistema."""

    def __init__(self) -> None:
        self._sensors: dict[str, dict] = {}

    def _validate_id(self, sensor_id: str) -> None:
        """Helper interno para validar que el ID no esté vacío."""
        if not sensor_id or not sensor_id.strip():
            raise ValueError("El ID del sensor no puede estar vacío.")

    def register(self, sensor_id: str, name: str) -> dict:
        """Registra un nuevo sensor en el sistema."""
        self._validate_id(sensor_id)

        sensor = {"id": sensor_id.strip(), "name": name.strip()}
        self._sensors[sensor_id.strip()] = sensor
        return dict(sensor)  # Retorno defensivo

    def get(self, sensor_id: str) -> dict:
        """Obtiene la información de un sensor registrado."""
        self._validate_id(sensor_id)

        clean_id = sensor_id.strip()
        if clean_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{clean_id}' no existe.")

        return dict(self._sensors[clean_id])  # Retorno defensivo
