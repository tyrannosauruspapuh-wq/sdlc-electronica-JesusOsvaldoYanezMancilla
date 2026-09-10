# ADR 0002: Validaciones de dominio y hardening de repositorios y modelos en SensorHub

## Estado
Aceptado

## Contexto
El análisis estático de código reveló múltiples riesgos de integridad, seguridad y rendimiento en las entidades `SensorModel` y `ReadingModel`, así como en sus repositorios:
- Invariantes de dominio no protegidos en sensores (rangos incoherentes `min_value > max_value`).
- Ausencia de restricciones e índices en `ReadingModel` (unidades sin límite de longitud `unit`, sin validación de valores `NaN`/infinitos, y falta de índice en `created_at`).
- Ausencia de validaciones de límites en paginación (`limit`, `offset`) e IDs negativos en capas de acceso a datos.
- Riesgos de seguridad (*Mass Assignment*) en el método `update` de repositorios al usar `setattr` dinámico sin restricciones.
- Consultas de filtrado por fechas en lecturas que fallaban silenciosamente o no validaban lógica de negocio (`from_date > to_date`).

## Decisión
1. **Validación defensiva y hardening en capa de dominio/modelo:** 
   - En `SensorModel`: Implementar validación para evitar persistir sensores con umbrales inválidos (`min_value > max_value`).
   - En `ReadingModel`: Restringir la longitud del campo `unit` (`String(50)`), agregar índice en `created_at` (o compuesto `sensor_id, created_at`) para optimizar búsquedas temporales, y asegurar que la marca de tiempo mantenga información de zona horaria (`timezone=True`).
2. **Whitelist para actualizaciones en repositorios:** Restringir explícitamente qué campos pueden ser modificados mediante `setattr` usando una lista blanca (`ALLOWED_UPDATE_FIELDS`) en `SensorRepository` para mitigar vulnerabilidades de *Mass Assignment*.
3. **Paginación y parámetros estrictos:** Agregar validaciones de rango explícitas en métodos de repositorio (`get_all`, `get_by_id`), lanzando `ValueError` cuando los parámetros violen límites razonables (`sensor_id <= 0`, `limit <= 0` o `limit > 1000`).
4. **Validación explícita de rangos temporales:** Validar en la capa de datos/servicio que `from_date` no sea posterior a `to_date` antes de ejecutar consultas SQL de lecturas.

## Consecuencias
+ **Protección contra vulnerabilidades de asignación masiva:** Se previene la modificación accidental o maliciosa de llaves primarias y marcas de tiempo (`created_at`).
+ **Mayor integridad de base de datos:** La entidad `ReadingModel` evita el almacenamiento de cadenas de texto arbitrariamente largas en `unit` e inconsistencias de zonas horarias.
+ **Rendimiento optimizado en consultas temporales:** La adición del índice en `created_at` evita escaneos completos de tabla (*full table scans*) en consultas por rango de fechas.
+ **Prevención de ataques DoS por memoria:** La limitación estricta de paginación en el repositorio evita lecturas masivas no autorizadas en la base de datos.
- **Acoplamiento ligero de reglas:** Requiere mantener alineados los esquemas Pydantic con las restricciones agregadas a la capa de repositorio y modelos.