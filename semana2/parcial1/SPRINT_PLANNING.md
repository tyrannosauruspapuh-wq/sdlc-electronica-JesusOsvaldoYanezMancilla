# Sprint Planning — Sprint 1 (Semana 2)

**Proyecto:** SensorHub  
**Sprint Goal:** Construir e implementar el núcleo del sistema de monitoreo IoT en Python con TDD, incluyendo el registro de sensores, validación de lecturas, detección de anomalías en tiempo real y emisión de alertas multicanal.

---

## Historias de Usuario Seleccionadas (Sprint Backlog)

Para este primer Sprint se han seleccionado **4 Historias de Usuario clave** (del nivel *Must Have*) que suman un total de **16 Story Points**:

| ID | Historia de Usuario | Story Points | Responsable |
| :--- | :--- | :---: | :--- |
| **US-01** | Registrar y consultar sensores en el sistema | 3 | Jesús Osvaldo |
| **US-02** | Registrar y validar lecturas de sensores | 3 | Jesús Osvaldo |
| **US-03** | Detección de anomalías en lecturas | 5 | Jesús Osvaldo |
| **US-04** | Emisión de alertas multicanal (Consola / Archivo) | 5 | Jesús Osvaldo |

---

## Desglose de Tareas por Historia (Tasks $\le 4\text{ h}$)

### US-01: Registrar y consultar sensores
* **Task 1.1:** Escribir pruebas unitarias en TDD para `SensorRegistry` (`register` y `get`) con manejo de duplicados y no encontrados ($\approx 1.5\text{ h}$).
* **Task 1.2:** Implementar la clase `SensorRegistry` y sus excepciones personalizadas `SensorAlreadyExistsError` y `SensorNotFoundError` ($\approx 1.5\text{ h}$).

### US-02: Registrar y validar lecturas de sensores
* **Task 2.1:** Diseñar la dataclass/modelo `SensorReading` con validación de tipos, rangos de temperatura/humedad y marcas de tiempo ($\approx 2\text{ h}$).
* **Task 2.2:** Escribir tests en TDD para el almacenamiento de lecturas vinculadas a un sensor existente ($\approx 1.5\text{ h}$).
* **Task 2.3:** Implementar el método de registro de lecturas validando que el sensor exista previamente ($\approx 1\text{ h}$).

### US-03: Detección de anomalías en lecturas
* **Task 3.1:** Crear tests para `AnomalyDetector` evaluando lecturas contra umbrales inyectados ($T > 35\text{ °C}$ o $H > 80\%$) ($\approx 2\text{ h}$).
* **Task 3.2:** Implementar `AnomalyDetector` garantizando que los umbrales no estén *hardcodeados* ($\approx 1.5\text{ h}$).

### US-04: Emisión de alertas multicanal
* **Task 4.1:** Definir la interfaz/protocolo abstracto `AlertStrategy` ($\approx 1\text{ h}$).
* **Task 4.2:** Escribir tests e implementar `ConsoleAlert` y `FileAlert` (escritura en `alerts.log`) ($\approx 2.5\text{ h}$).
* **Task 4.3:** Implementar `AlertManager` para coordinar el envío a múltiples estrategias al detectar una anomalía ($\approx 2\text{ h}$).

---

## Definition of Done (DoD) Aplicable

Una historia de usuario se considerará **DONE** cuando cumpla con todos los criterios establecidos en el documento general de la semana (`semana2/DEFINITION_OF_DONE.md`):

1. **Pruebas:** 100% de los tests unitarios ejecutados mediante `pytest` pasan en verde.
2. **Cobertura:** La cobertura de código en el módulo `semana2/` es $\ge 80\%$.
3. **Calidad de Código:** El código pasa la revisión de **Ruff** sin errores ni advertencias (`ruff check .`).
4. **Tipado Estático:** El verificador **mypy** confirma anotaciones de tipo válidas (`mypy semana2/`).
5. **Documentación:** Todas las clases y funciones públicas incluyen *docstrings* explicativos.