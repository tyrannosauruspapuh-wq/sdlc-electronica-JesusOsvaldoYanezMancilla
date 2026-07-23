# Definition of Done (DoD) - Semana 2

Para considerar que una User Story o funcionalidad está terminada (**DONE**), debe cumplir con la siguiente lista de verificación:

## Checklist de Calidad
- [ ] **Tests Unitarios:** Todos los tests pasan exitosamente (`pytest`).
- [ ] **Cobertura de Código:** La cobertura de código es igual o mayor al **80%** (`pytest --cov`).
- [ ] **Linting & Formato:** El código cumple con las reglas de **Ruff** sin advertencias ni errores (`ruff check .`).
- [ ] **Verificación de Tipos:** **mypy** no reporta errores de tipos ni funciones no tipadas (`mypy semana2/`).
- [ ] **Revisión de Código:** Auto-revisión del diff en el Pull Request antes de hacer merge a `main`.
- [ ] **Documentación:** Docstrings actualizados en clases y métodos públicos.

## Criterios de Aceptación (Gherkin)

### Escenario 1: Registro exitoso de un sensor
```gherkin
Given que el sistema de registro de sensores está inicializado
When registro un sensor con ID "TEMP-01" y nombre "Sensor Bodega"
Then el sensor se almacena correctamente
And al consultar "TEMP-01" obtengo la información del sensor registrado

### Escenario 2: Intento de registrar un sensor duplicado

Given que el sensor "TEMP-01" ya está registrado
When intento registrar un nuevo sensor con ID "TEMP-01"
Then el sistema lanza una excepción SensorAlreadyExistsError

### Escenario 3: Consulta de sensor inexistente

Given que el sensor "GHOST-99" no ha sido registrado
When intento consultar el sensor "GHOST-99"
Then el sistema lanza una excepción SensorNotFoundError