# Día 1: Prompting Efectivo para SensorHub API

Análisis comparativo de prompts pobres vs. prompts bien estructurados aplicados a tareas reales del desarrollo de SensorHub API.

---

## Tarea 1: Detección de Anomalías por Umbrales (Lógica de Negocio)

### Prompt Pobre

> "Hazme una funcion que revise si una lectura de temperatura esta fuera de rango y lance error"

#### Resultado Obtenido (Prompt Pobre)

```python
def check_temp(val):
    if val < 0 or val > 100:
        raise Exception("Temperatura invalida")
    return True
```

**Análisis del fallo:** La función usa valores fijos (hardcoded), no soporta diferentes tipos de sensores ni umbrales dinámicos, usa excepciones genéricas en lugar de Pydantic/FastAPI, y carece de type hints.

### Custom Prompt Bueno

```plaintext
CONTEXTO: API FastAPI (Python 3.12) para SensorHub. Arquitectura en capas con Pydantic v2.
TAREA: Escribe una función pura `check_threshold_anomaly(value: float, min_val: float, max_val: float) -> bool` para detectar si una lectura viola los umbrales configurados.
RESTRICCIONES: Type hints completos, docstring explicativo con Google Style, manejo de tipos numéricos estrictos, retorna True si es anomalía (fuera de rango) o False si está OK.
ENTREGA: Solo el código de la función en Python, sin explicaciones adicionales.
```

#### Resultado Obtenido (Prompt Bueno)

```python
def check_threshold_anomaly(value: float, min_val: float, max_val: float) -> bool:
    """Evalúa si una lectura dada se encuentra fuera del rango permitido.

    Args:
        value (float): Valor numérico de la lectura registrada.
        min_val (float): Umbral mínimo permitido para el sensor.
        max_val (float): Umbral máximo permitido para el sensor.

    Returns:
        bool: True si la lectura supera el límite superior o está por debajo
              del límite inferior (anomalía); False en caso contrario.
    """
    return value < min_val or value > max_val
```

**Análisis del éxito:** Es una función pura, totalmente reutilizable para cualquier tipo de sensor (temperatura, humedad, presión), incluye tipado estricto y un docstring claro sin código innecesario.

---

## Tarea 2: Endpoint para Consulta de Alertas de Sensores

### Prompt Pobre

> "Dame el endpoint para ver las alertas de la base de datos en fastapi"

#### Resultado Obtenido (Prompt Pobre)

```python
@app.get("/alerts")
def get_alerts():
    db = sqlite3.connect("database.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM alerts")
    return cursor.fetchall()
```

**Análisis del fallo:** Usa sqlite3 directamente en lugar del ORM de SQLAlchemy 2.0, ignora la inyección de dependencias (`Depends(get_db)`), no valida las respuestas con Pydantic y mezcla capas de acceso a datos en la ruta.

### Custom Prompt Bueno

```plaintext
CONTEXTO: API FastAPI (Python 3.12) para SensorHub. SQLAlchemy 2.x asíncrono/síncrono con Session inyectada via `get_db`.
TAREA: Escribe un endpoint GET `/sensors/{sensor_id}/alerts` dentro de un APIRouter que obtenga la lista de alertas asociadas a un sensor específico.
RESTRICCIONES: Retornar tipo list[AlertResponse] (esquema Pydantic), manejar error HTTP 404 si el sensor no existe, usar `select()` de SQLAlchemy 2.0.
ENTREGA: Solo la definición de la ruta con sus dependencias e imports necesarios, sin texto explicativo.
```

#### Resultado Obtenido (Prompt Bueno)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.alert import Alert
from app.models.sensor import Sensor
from app.schemas.alert import AlertResponse

router = APIRouter(prefix="/sensors", tags=["Alerts"])

@router.get("/{sensor_id}/alerts", response_model=list[AlertResponse])
def get_sensor_alerts(sensor_id: int, db: Session = Depends(get_db)) -> list[Alert]:
    sensor = db.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor con ID {sensor_id} no encontrado.",
        )

    stmt = select(Alert).where(Alert.sensor_id == sensor_id)
    alerts = db.scalars(stmt).all()
    return list(alerts)
```

**Análisis del éxito:** Integra la arquitectura existente del proyecto (SQLAlchemy 2.0 + Pydantic + FastAPI Depends), maneja adecuadamente errores HTTP 404 y respeta las convenciones del repositorio.

---

## Tarea 3: Conversión de Unidades de Lecturas (Función Útil)

### Prompt Pobre

> "Hazme una funcion en python que convierta de celsius a fahrenheit"

#### Resultado Obtenido (Prompt Pobre)

```python
def conv(c):
    return (c * 9/5) + 32
```

**Análisis del fallo:** Nombres de variables crípticos (`conv`, `c`), sin redondeo, sin type hints y sin documentación.

### Custom Prompt Bueno

```plaintext
CONTEXTO: API FastAPI (Python 3.12) para gestión de sensores. SQLAlchemy 2.x tipado, arquitectura en capas.
TAREA: Escribe una función pura `celsius_to_fahrenheit(c: float) -> float` en `semana5/conversions.py`.
RESTRICCIONES: Type hints completos, docstring, sin dependencias externas, redondeo a 2 decimales.
ENTREGA: Solo la función, sin explicación.
```

#### Resultado Obtenido (Prompt Bueno)

```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convierte una temperatura de grados Celsius a Fahrenheit.

    Args:
        c (float): Temperatura en grados Celsius.

    Returns:
        float: Temperatura equivalente en grados Fahrenheit redondeada a 2 decimales.
    """
    fahrenheit = (c * 9 / 5) + 32
    return round(fahrenheit, 2)
```

**Análisis del éxito:** Cumple al 100% las restricciones requeridas, entrega código listo para producción y libre de sobrecargas de texto.