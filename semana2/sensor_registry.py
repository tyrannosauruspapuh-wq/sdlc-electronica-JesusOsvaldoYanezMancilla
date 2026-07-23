
##Código de testeo para la semana 2
##Autor: Jesús Osvaldo Yáñez Mancilla
class SensorNotFoundError(Exception):
    """Excepción lanzada cuando un sensor no existe en el registro."""
    pass


class SensorAlreadyExistsError(Exception):
    """Excepción lanzada cuando se intenta registrar un sensor con un ID duplicado."""
    pass


class SensorRegistry:

    def __init__(self) -> None:
        self._sensors: dict[str, dict] = {}

    def register(self, sensor_id: str, name: str) -> dict:
        clean_id = sensor_id.strip()
        
        # Validar si el sensor ya existe
        if clean_id in self._sensors:
            raise SensorAlreadyExistsError(f"El sensor con ID '{clean_id}' ya está registrado.")

        sensor = {"id": clean_id, "name": name.strip()}
        self._sensors[clean_id] = sensor
        return dict(sensor)

    def get(self, sensor_id: str) -> dict:
        clean_id = sensor_id.strip()
        if clean_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{clean_id}' no existe.")
        return dict(self._sensors[clean_id])