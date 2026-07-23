# Product Backlog — SensorHub

## Sprint Bakclog (sprint 1)
> Historias seleccionadas para realizar en este sprint.

## US-01: Registrar lectura de sensor
**Como** operador de planta,  
**quiero** registrar la lectura de un sensor con su timestamp,  
**para** tener un historial consultable de las mediciones.

### Scenario: Registrar una lectura válida
- **Given** un sensor con id "TEMP-01" registrado en el sistema
- **When** envío una lectura de 24.3 C con timestamp actual
- **Then** la lectura se guarda con estado "OK"
- **And** puedo me muestra la confirmación con el ID generado

### Scenario: Rechazar lectura de sensor inexistente
- **Given** que no existe ningún sensor con id "GHOST-99"
- **When** envío una lectura para "GHOST-99"
- **Then** el sistema responde con un error 404
- **And** no se guarda ningún registro en la base de datos

---

## Product Backlog (Futuros Sprints)
> Historias pendientes a hacer en el siguiente Sprint

## US-02: Consultar historial de un sensor
**Como** analista de mantenimiento,  
**quiero** obtener todas las lecturas de un sensor en un rango de tiempo,  
**para** analizar el comportamiento térmico del equipo.

### Scenario: Obtener lecturas en un rango válido
- **Given** que existen 10 lecturas registradas para "TEMP-01"
- **When** solicito las lecturas entre "2026-07-01" y "2026-07-22"
- **Then** el sistema devuelve una lista con las lecturas de ese periodo
- **And** el código de respuesta HTTP es 200 OK

### Scenario: Rango de fechas sin lecturas
- **Given** que no hay lecturas para "TEMP-01" en el rango solicitado
- **When** solicito las lecturas del periodo
- **Then** el sistema devuelve una lista vacía `[]` con código 200 OK

---

## US-03: Alerta por sobretemperatura
**Como** sistema de monitoreo,  
**quiero** detectar cuando una lectura supera el umbral máximo,  
**para** generar un evento de advertencia inmediatamente.

### Scenario: Lectura supera el umbral crítico
- **Given** un umbral configurado de 80.0 C para el sensor "TEMP-01"
- **When** se recibe una lectura de 85.5 C
- **Then** la respuesta incluye la bandera `is_anomaly: true`
- **And** se registra una entrada de alerta en la bitácora de eventos
