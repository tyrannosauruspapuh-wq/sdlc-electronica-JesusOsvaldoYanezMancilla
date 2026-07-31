# 2. Convenciones REST y Manejo de Errores para Lecturas de Sensores

* **Estado:** Aceptado
* **Fecha:** 2026-07-30
* **Autor:** Jesús Osvaldo Yáñez Mancilla

## Contexto
El sistema SensorHub requiere una API HTTP para la gestión de lecturas de sensores. Para mantener interoperabilidad, predecibilidad y alineación con los estándares web, es necesario definir la estructura de rutas, los verbos HTTP correspondientes y la estrategia de respuesta ante recursos no encontrados o creación exitosa.

## Decisión
Hemos decidido implementar las siguientes convenciones REST en el endpoint `/readings`:

1. **`POST /readings`**: Creación de nuevas lecturas de sensores. Retorna un código HTTP `201 Created` con el objeto completo generado (incluyendo `id` autoincrementable y `created_at`).
2. **`GET /readings`**: Consulta y listado general de lecturas. Retorna un código HTTP `200 OK` con la lista de registros guardados.
3. **`GET /readings/{reading_id}`**: Búsqueda individual de lecturas por ID.
   * Si el registro existe, retorna `200 OK` con los datos del sensor.
   * Si el registro no existe, lanza un `HTTPException` con código `404 Not Found` y un mensaje explícito en el cuerpo JSON.

## Alternativas consideradas
* **Devolver arreglos vacíos o `null` en lugar de 404:** Se descartó porque no sigue el estándar HTTP, ocultando el estado real del recurso y dificultando la depuración en clientes web o móviles.
* **Usar `200 OK` para la creación (`POST`):** Se descartó en favor de `201 Created`, que especifica explícitamente la persistencia y generación de un nuevo recurso.

## Consecuencias
* **Positivas:** 
  * Respuestas semánticamente correctas y predecibles alineadas al estándar OpenAPI/Swagger.
  * Facilidad para pruebas integradas manuales (Swagger UI) y automatizadas con `TestClient`.
  * Integración transparente con Pydantic y SQLAlchemy mediante `response_model` y manejo de excepciones de FastAPI.
* **Negativas / Limitaciones:**
  * Requiere manejar de forma explícita las excepciones `HTTPException` en las capas superiores cuando un recurso no se encuentra en la base de datos.