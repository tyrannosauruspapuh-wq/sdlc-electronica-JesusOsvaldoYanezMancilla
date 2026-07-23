
##Código de testeo para la semana 2
##Autor: Jesús Osvaldo Yáñez Mancilla
class SensorNotFoundError(Exception):
    """Excepción cuando un sensor no existe en el registro."""

    pass


class SensorRegistry:

    def __init__(self) -> None:
        self._sensors: dict[str, dict] = {}

    def get(self, sensor_id: str) -> dict:
        if sensor_id not in self._sensors:
            raise SensorNotFoundError(f"El sensor '{sensor_id}' no existe.")
        return self._sensors[sensor_id]

