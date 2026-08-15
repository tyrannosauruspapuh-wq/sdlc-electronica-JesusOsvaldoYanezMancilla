# Documentación de 2 carpetas de app/

## Revisión de models/

**m_reading.py**


No veo una violación fuerte de SOLID en esta clase: es un modelo ORM con responsabilidad clara y sin lógica de negocio compleja. Sí hay varios riesgos de integridad, validación y rendimiento.

### Hallazgos relevantes

1. Validación insuficiente de `value` y `unit`  
   - Línea: `m_reading.py:16-19`  
   - Problema: `value` acepta cualquier `float`, y `unit` acepta cualquier cadena. Eso permite valores `NaN`, infinitos, unidades no soportadas o cadenas muy largas, lo que puede romper cálculos, métricas o reportes.  
   - Corrección: validar en la capa de dominio/servicio o restringir en el ORM con un conjunto permitido (`Enum`) y rechazar `NaN`/`inf` antes de persistir.

2. Fuga de integridad referencial en `sensor_id`  
   - Línea: `m_reading.py:13-14`  
   - Problema: hay `ForeignKey`, pero no está configurado el comportamiento de borrado del lado de la base de datos. Si un `SensorModel` se elimina y la relación no está bien gestionada, la BD puede fallar o dejar datos inconsistentes.  
   - Corrección: definir `ondelete="CASCADE"` o garantizar la eliminación en la capa de servicio con transacción explícita.

3. Riesgo de almacenamiento / abuso por `unit` sin longitud ni restricción  
   - Línea: `m_reading.py:17`  
   - Problema: `String` sin longitud permite cadenas arbitrariamente grandes. Esto puede provocar crecimiento excesivo de la base de datos y, en escenarios de entrada no controlada, abuso de espacio o errores de serialización.  
   - Corrección: limitar longitud (`String(10)` o similar) o usar `Enum` si el conjunto de valores es fijo.

4. Falta de índice para consultas por tiempo  
   - Línea: `m_reading.py:18-20`  
   - Problema: `created_at` no tiene `index=True`. Si el sistema consulta rangos temporales (últimas horas, por día, historial), la consulta puede degradar mucho con volumen medio/alto.  
   - Corrección: añadir índice a `created_at` o mejor aún a un índice compuesto como `(sensor_id, created_at)` si ese patrón es común.

5. Posible inconsistencia de timezone al persistir marcas temporales  
   - Línea: `m_reading.py:18-20`  
   - Problema: usas `datetime.now(UTC)`, que está bien, pero el campo `DateTime` no indica explícitamente timezone-aware en la base de datos. Si la BD o drivers trabajan con datetime naive, puedes introducir inconsistencias de horario al guardar/leer.  
   - Corrección: usar `DateTime(timezone=True)` y/o `server_default` según la configuración de la BD para garantizar UTC consistente.

6. Desacoplamiento de reglas de validación de dominio  
   - Línea: `m_reading.py:16-23`  
   - Problema: la clase no enforces la regla “el valor debe estar dentro del rango del sensor” ni “la unidad debe corresponder al tipo de sensor”, aunque eso es crucial para la integridad del dominio. Si esto queda solo en la capa de API, cualquier inserción directa a la DB puede romper la lógica.  
   - Corrección: centralizar la validación en el servicio o en un validador de dominio antes del `commit`, y no confiar solo en el `ORM`.

### Conclusión
El modelo es simple y legible, pero el principal riesgo no es “SOLID” sino la falta de validación y restricciones de integridad. Si quieres, puedo hacer una segunda pasada enfocada solo en la capa de servicio/repository para identificar qué validaciones deberían moverse fuera del modelo sin reescribir todo.

---

# **m_sensor.py**


He identificado varios hallazgos. Aquí está el análisis:



### 🔴 **SOLID - Falta de Validación (Single Responsibility)**

**Línea 15-16:** `min_value` y `max_value` no tienen validación de lógica
```python
min_value: Mapped[float] = mapped_column(Float, nullable=False)
max_value: Mapped[float] = mapped_column(Float, nullable=False)
```
**Problema:** No hay garantía de que `min_value <= max_value`. Se viola el invariante de dominio.

**Propuesta:**
```python
@validates('min_value', 'max_value')
def validate_range(self, key, value):
    if value is None:
        raise ValueError(f"{key} no puede ser None")
    if hasattr(self, 'min_value') and hasattr(self, 'max_value'):
        if self.min_value > self.max_value:
            raise ValueError("min_value no puede ser mayor que max_value")
    return value
```

---

### 🔴 **Casos Borde: Strings Vacíos (Línea 11-13)**

```python
name: Mapped[str] = mapped_column(String, nullable=False)
type: Mapped[str] = mapped_column(String, nullable=False)
unit: Mapped[str] = mapped_column(String, nullable=False)
```
**Problema:** `nullable=False` no previene strings vacíos. `name=""` se acepta pero es inválido.

**Propuesta:**
```python
name: Mapped[str] = mapped_column(String(255), nullable=False)  # Agregar límite
type: Mapped[str] = mapped_column(String(50), nullable=False)   # Restringir longitud
unit: Mapped[str] = mapped_column(String(50), nullable=False)

@validates('name', 'type', 'unit')
def validate_non_empty(self, key, value):
    if not value or not value.strip():
        raise ValueError(f"{key} no puede estar vacío")
    return value.strip()
```

---

### 🟡 **Riesgo de Seguridad: Cascada Silenciosa (Línea 18-21)**

```python
cascade="all, delete-orphan",
```
**Problema:** Eliminar un sensor borra automáticamente todas sus lecturas sin auditoría ni confirmación. Posible pérdida de datos críticos.

**Propuesta:**
```python
# Opción 1: Usar soft-delete o marcar como inactivo
cascade="save-update, merge",  # Sin delete automático

# Opción 2: Implementar un check antes de permitir la eliminación
@event.listens_for(SensorModel, "before_delete")
def receive_before_delete(mapper, connection, target):
    raise ValueError(f"No se puede eliminar sensor {target.id} con lecturas activas")
```

---

### 🟡 **Rendimiento: N+1 Queries Potencial (Línea 18-21)**

```python
readings = relationship(
    "ReadingModel",
    back_populates="sensor",
    cascade="all, delete-orphan",
)
```
**Problema:** Sin especificar `lazy`, SQLAlchemy usará el default que puede causar queries extras al acceder a `sensor.readings`.

**Propuesta:**
```python
readings = relationship(
    "ReadingModel",
    back_populates="sensor",
    cascade="all, delete-orphan",
    lazy="selectin",  # O "joined" según caso de uso
)
```

---

### 🟡 **Rendimiento: Falta de Índices (Línea 11-13)**

**Problema:** `name` y `type` probablemente se usan en filtros/búsquedas, pero no tienen índice.

**Propuesta:**
```python
name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
```

---

## 🟡 **Type Hints: Falta `__init__` Explícito**

**Problema:** Sin `__init__`, es difícil documentar y validar parámetros al crear instancias.

**Propuesta:**
```python
def __init__(self, name: str, type: str, unit: str, min_value: float, max_value: float):
    if min_value > max_value:
        raise ValueError("min_value debe ser menor o igual a max_value")
    self.name = name.strip()
    self.type = type.strip()
    self.unit = unit.strip()
    self.min_value = min_value
    self.max_value = max_value
```

---

## **Lo que sí está bien:**
- Uso de `Mapped` y `mapped_column` (moderno)
- Relationship correctamente configurado
- `autoincrement=True` apropiado para PK



---

# Revisión de repositories/

## **reading_repo.py**


### 🔴 **VIOLACIONES DE SOLID**

### Líneas 22-41 - Responsabilidad única comprometida
El método `get_by_sensor()` acumula múltiples responsabilidades: validación de rango de fechas, paginación y filtrado. Considere extraer validación a un servicio o usar un patrón Query Object.

```python
# Propuesta: Validar en nivel superior
if from_date and to_date and from_date > to_date:
    raise ValueError("from_date debe ser menor a to_date")
```

---

###  **CASOS BORDE SIN MANEJAR**

### Línea 28 - `get_by_sensor()` sin validación de sensor_id
**Riesgo:** Acepta cualquier `sensor_id`, incluso inválidos. No valida que el sensor exista.
```python
# Propuesta: Validar antes de query
if sensor_id <= 0:
    raise ValueError("sensor_id debe ser positivo")
```

### Línea 30-31 - Sin validación de rango de fechas
**Riesgo:** Si `from_date > to_date`, la query retorna vacío sin error.
```python
# Propuesta: Agregar validación
if from_date and to_date and from_date > to_date:
    raise ValueError("Rango de fechas inválido")
```

### Línea 43-47 - `delete()` sin validar restricciones de integridad
**Riesgo:** Si hay FK constraints, el delete falla silenciosamente. El `bool` no indica por qué falló.
```python
# Propuesta: Diferenciar causas de fallo
try:
    self.session.delete(db_reading)
    self.session.commit()
    return True
except IntegrityError:
    self.session.rollback()
    raise ValueError("No se puede eliminar: hay referencias")
```

---

###  **RIESGOS DE SEGURIDAD**

### Línea 13-17 - `create()` sin manejo de excepciones
**Riesgo:** Excepciones de BD (IntegrityError, DataError) se propagan sin encapsular. Podrían exponer detalles internos.
```python
# Propuesta: Capturar y re-lanzar controladamente
try:
    self.session.add(db_reading)
    self.session.commit()
except IntegrityError as e:
    self.session.rollback()
    raise ValueError("Lectura duplicada o datos inválidos") from e
```

### Línea 43-48 - `delete()` sin validación de permisos
**Riesgo:** No valida si el usuario tiene permisos para borrar esta lectura (aunque sea responsabilidad del router, el repo debe ser defensivo).

---

###  **PROBLEMAS DE RENDIMIENTO**

### Línea 43-48 - `delete()` hace dos queries
**Riesgo:** Una query de SELECT (`get_by_id`) + una de DELETE. Podría ser una sola.
```python
# Propuesta: Usar DELETE directo
def delete(self, reading_id: int) -> bool:
    stmt = delete(ReadingModel).where(ReadingModel.id == reading_id)
    result = self.session.execute(stmt)
    self.session.commit()
    return result.rowcount > 0
```

### Línea 17 - `refresh()` innecesario
**Riesgo:** La línea `self.session.refresh(db_reading)` ejecuta una query extra si no necesitas datos actualizados (timestamps, IDs auto-generados).
```python
# Propuesta: Evaluar si es realmente necesario. Si solo necesitas el ID:
self.session.flush()  # Asegura que se asigne el ID
return db_reading
```

---

###  **RESUMEN DE ACCIONES**

| Línea | Tipo | Severidad | Acción |
|-------|------|-----------|--------|
| 13-17 | Excepciones | 🔴 Alta | Manejar IntegrityError, DataError |
| 28 | Validación | 🟡 Media | Validar sensor_id > 0 |
| 30-31 | Lógica | 🟡 Media | Validar from_date ≤ to_date |
| 43-48 | Rendimiento | 🟡 Media | Usar DELETE directo en lugar de get + delete |
| 43-48 | Seguridad | 🟡 Media | Distinguir "no existe" vs "error de BD" |
---


## **sensor_repo.py**




### **VIOLACIONES DE SOLID**

### 🔴 Dependency Inversion (Líneas 13-15)
```python
def __init__(self, session: Session) -> None:
    self.session = session
```
**Problema:** La clase depende directamente de `Session` de SQLAlchemy. Hace el código acoplado y difícil de testear.

**Propuesta:** Crear una interfaz `IDataSession` y que el repository la implemente:
```python
from abc import ABC, abstractmethod

class IDataSession(ABC):
    @abstractmethod
    def execute(self, ...): pass
    @abstractmethod
    def commit(self): pass
```

---

### **CASOS BORDE SIN MANEJAR**

### 🟡 Línea 19 - `get_all()`: Parámetros sin validación
```python
def get_all(self, limit: int = 100, offset: int = 0) -> list[SensorModel]:
```
**Problemas:**
- No valida `limit` y `offset` negativos
- No valida límite superior (alguien podría pedir `limit=1_000_000`)
- Default de 100 es arbitrario

**Propuesta:**
```python
def get_all(self, limit: int = 100, offset: int = 0) -> list[SensorModel]:
    if limit <= 0 or offset < 0:
        raise ValueError("limit debe ser > 0 y offset >= 0")
    if limit > 1000:  # máximo razonable
        raise ValueError("limit excede máximo permitido")
```

---

### 🟡 Línea 24 - `get_by_id()`: Falta validación de ID
```python
def get_by_id(self, sensor_id: int) -> SensorModel | None:
```
**Problema:** No valida si `sensor_id` es positivo (IDs negativos no tienen sentido).

**Propuesta:**
```python
if sensor_id <= 0:
    raise ValueError("sensor_id debe ser positivo")
```

---

### 🟡 Línea 28 - `create()`: Falta manejo de excepciones
```python
def create(self, sensor_data: SensorCreate) -> SensorModel:
    db_sensor = SensorModel(**sensor_data.model_dump())
    self.session.add(db_sensor)
    self.session.commit()  # ¿Y si hay constraint violation?
    self.session.refresh(db_sensor)
    return db_sensor
```
**Problemas:**
- No captura `IntegrityError` (duplicado, FK constraint)
- No captura excepciones de conexión
- No hace rollback en error

**Propuesta:**
```python
try:
    self.session.add(db_sensor)
    self.session.commit()
except IntegrityError as e:
    self.session.rollback()
    raise ValueError(f"Violación de constraint: {e}") from e
except Exception as e:
    self.session.rollback()
    raise
```

---

### 🟡 Línea 35 - `update()`: Múltiples problemas
```python
def update(self, sensor_id: int, sensor_data: SensorUpdate) -> SensorModel | None:
    db_sensor = self.get_by_id(sensor_id)  # Query 1
    if not db_sensor:
        return None
    
    update_dict = sensor_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_sensor, key, value)  # ⚠️ Seguridad
    
    self.session.commit()  # Sin manejo de error
    self.session.refresh(db_sensor)
    return db_sensor
```

**Problemas:**
- Dos queries por actualizaciónón (get + commit) = ineficiente
- `setattr` permite inyectar atributos arbitrarios (si `update_dict` contiene claves no esperadas)
- Sin manejo de excepciones

---

### 🟡 Línea 44 - `delete()`: Sin validación de ID
```python
def delete(self, sensor_id: int) -> bool:
```
**Mismo problema que `get_by_id()`**: no valida `sensor_id > 0`.

---

### **RIESGOS DE SEGURIDAD**

### 🔴 Línea 40 - `setattr()` sin whitelist
```python
for key, value in update_dict.items():
    setattr(db_sensor, key, value)
```
**Riesgo:** Si `SensorUpdate` schema es mal diseñado, alguien podría actualizar campos que no debería (ej: `created_at`, `user_id`).

**Propuesta:** Validar explícitamente qué campos pueden actualizarse:
```python
ALLOWED_UPDATE_FIELDS = {"name", "location", "status"}
for key, value in update_dict.items():
    if key not in ALLOWED_UPDATE_FIELDS:
        raise ValueError(f"Campo '{key}' no puede actualizarse")
    setattr(db_sensor, key, value)
```

---

### 🟡 Falta auditoría
**Problema:** No hay registro de quién creó/actualizó/eliminó cada sensor.

**Propuesta:** Agregar timestamps y usuario en el modelo:
```python
created_by: int
updated_by: int | None
created_at: datetime
updated_at: datetime
```

---

### **PROBLEMAS DE RENDIMIENTO**

### 🟡 Línea 19 - Paginación ineficiente por defecto
El `limit=100` es demasiado alto para un endpoint default. La mayoría de UIs no mostrarían 100 elementos.

**Propuesta:** Reducir a 20-50, o hacerlo configurable.

---

### 🟡 Línea 35 & 44 - N+1 queries en `update()` y `delete()`
```python
db_sensor = self.get_by_id(sensor_id)  # Query 1: SELECT
# ... 
self.session.commit()  # Query 2: UPDATE o DELETE
```

**Propuesta:** Usar bulk operations:
```python
def delete(self, sensor_id: int) -> bool:
    result = self.session.execute(
        delete(SensorModel).where(SensorModel.id == sensor_id)
    )
    self.session.commit()
    return result.rowcount > 0
```

---

### 🟡 Línea 39 - `model_dump()` innecesario
```python
update_dict = sensor_data.model_dump(exclude_unset=True)
```
Si solo necesitas los campos actualizados, considera validar directamente en el schema Pydantic.

---

## **RESUMEN DE PRIORIDADES**

| Severidad | Líneas | Tipo |
|-----------|--------|------|
| 🔴 Alta | 13-15, 40 | Acoplamiento + Seguridad |
| 🟡 Media | 19, 24, 28, 35, 44 | Validación + Excepciones |
| 🟢 Baja | 39, defaults | Performance |

¿Quieres que implemente alguna de estas correcciones?