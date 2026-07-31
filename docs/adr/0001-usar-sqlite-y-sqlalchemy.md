# 1. Usar SQLite y SQLAlchemy 2.x para persistencia de datos

* **Estado:** Aceptado
* **Fecha:** 2026-07-30
* **Autor:** [Tu Nombre]

## Contexto
El sistema SensorHub requiere almacenar lecturas de sensores de manera persistente. En las fases iniciales del proyecto necesitamos una base de datos ligera, fácil de configurar en entornos locales y de desarrollo sin dependencias complejas de infraestructura.

## Decisión
Hemos decidido utilizar **SQLite** como motor de base de datos relacional para el entorno local y **SQLAlchemy 2.x** como ORM (Object-Relational Mapping).

## Alternativas consideradas
1. **Guardar en archivos JSON / CSV:** Fácil de implementar, pero carece de transacciones, consultas eficientes por índices y consistencia de datos.
2. **PostgreSQL desde el Día 1:** Excelente para producción, pero agrega complejidad innecesaria de instalación y contenedores en la fase inicial de desarrollo local.

## Consecuencias
* **Positivas:** 
  * Cero configuración de servidores adicionales (archivo `sensorhub.db` local).
  * Fácil integración con FastAPI mediante `sessionmaker` y `Depends()`.
  * Definición clara de modelos mediante la sintaxis moderna `Mapped[...]` de SQLAlchemy 2.x.
* **Negativas / Limitaciones:**
  * No soporta concurrencia alta de escrituras simultáneas 