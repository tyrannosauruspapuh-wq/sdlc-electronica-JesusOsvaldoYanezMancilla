# Product Backlog — SensorHub

## Sprint Backlog (Sprint 1)
> Historias seleccionadas para realizar en este sprint.

## US-01: Registrar y consultar sensores en el sistema
**Como** administrador de la bodega,  
**quiero** registrar sensores en el sistema con su ID, tipo y ubicación,  
**para** gestionar los dispositivos activos en la planta.

### Scenario: Registro exitoso de un sensor
- **Given** que el registro de sensores está vacío
- **When** registro un sensor con ID "TEMP-01", tipo "TEMPERATURE" y ubicación "Zona A"
- **Then** el sensor queda guardado en la memoria
- **And** puedo consultar "TEMP-01" obteniendo sus datos correspondientes

### Scenario: Error al registrar sensor duplicado
- **Given** que el sensor "TEMP-01" ya existe en el registro
- **When** intento registrar nuevamente un sensor con ID "TEMP-01"
- **Then** el sistema lanza una excepción `SensorAlreadyExistsError`

---

## US-02: Registrar y validar lecturas de sensores
**Como** operador de planta,  
**quiero** registrar la lectura de un sensor con su timestamp y valor,  
**para** garantizar que los datos guardados en el sistema sean válidos y coherentes.

### Scenario: Registrar una lectura válida
- **Given** un sensor con ID "TEMP-01" registrado en el sistema
- **When** envío una lectura de 24.3 °C con timestamp actual
- **Then** la lectura se almacena correctamente en el historial del sensor
- **And** me muestra la confirmación del registro exitoso

### Scenario: Rechazar lectura de sensor inexistente
- **Given** que no existe ningún sensor con ID "GHOST-99"
- **When** envío una lectura para "GHOST-99"
- **Then** el sistema lanza una excepción `SensorNotFoundError`
- **And** no se guarda ningún registro en la base de datos

---

## US-03: Detección de anomalías en lecturas
**Como** sistema de monitoreo,  
**quiero** detectar cuando una lectura supera los umbrales máximos (T > 35 °C o H > 80%),  
**para** clasificar la medición como una anomalía en tiempo real.

### Scenario: Lectura supera el umbral crítico de temperatura
- **Given** un umbral de temperatura máxima configurado de 35.0 °C
- **When** el detector evalúa una lectura de 38.2 °C del sensor "TEMP-01"
- **Then** la lectura es clasificada como anomalía (`is_anomaly: true`)

### Scenario: Lectura dentro del rango normal
- **Given** un umbral de temperatura máxima configurado de 35.0 °C
- **When** el detector evalúa una lectura de 22.0 °C del sensor "TEMP-01"
- **Then** la lectura es clasificada como normal (`is_anomaly: false`)

---

## US-04: Emisión de alertas multicanal
**Como** supervisor de seguridad,  
**quiero** recibir alertas automáticas en consola y en un archivo de log cuando se detecte una anomalía,  
**para** enterarme de inmediato y tener evidencia auditable.

### Scenario: Emisión de alerta por consola y archivo
- **Given** un gestor de alertas configurado con las estrategias de Consola y Archivo
- **When** se detecta una anomalía en la lectura del sensor "TEMP-01"
- **Then** la alerta se imprime en la consola estándar
- **And** se escribe un nuevo registro de advertencia en el archivo `alerts.log`

---

## Product Backlog (Futuros Sprints)
> Historias pendientes a hacer en los siguientes Sprints.

## US-05: Consultar historial de un sensor
**Como** analista de mantenimiento,  
**quiero** obtener todas las lecturas de un sensor registradas en un rango de tiempo,  
**para** analizar el comportamiento térmico u hídrico del equipo.

### Scenario: Obtener lecturas en un rango válido
- **Given** que existen 10 lecturas registradas para "TEMP-01"
- **When** solicito las lecturas entre "2026-07-01" y "2026-07-22"
- **Then** el sistema devuelve una lista con las 10 lecturas de ese periodo
- **And** el código de respuesta HTTP es 200 OK

### Scenario: Rango de fechas sin lecturas
- **Given** que no hay lecturas para "TEMP-01" en el rango solicitado
- **When** solicito las lecturas del periodo
- **Then** el sistema devuelve una lista vacía `[]` con código 200 OK

---

## US-06: Cálculo de estadísticas básicas por sensor
**Como** administrador de planta,  
**quiero** consultar la temperatura o humedad promedio y máxima registrada en un periodo,  
**para** evaluar el rendimiento general de la zona monitoreada.

### Scenario: Obtención del valor máximo de un sensor
- **Given** que el sensor "TEMP-01" tiene lecturas de [20.0, 25.5, 30.0] °C
- **When** solicito el valor máximo registrado
- **Then** el sistema retorna 30.0 °C
- **And** calcula un promedio de 25.16 °C

---

## US-07: Configuración dinámica de umbrales
**Como** operador del sistema,  
**quiero** modificar los umbrales de alerta de forma dinámica sin modificar el código fuente,  
**para** adaptar las alertas a diferentes temporadas del año o tipos de mercancía.

### Scenario: Modificación de umbral de alerta
- **Given** un detector con umbral inicial de 35.0 °C
- **When** actualizo el umbral de temperatura a 30.0 °C
- **Then** una lectura posterior de 32.0 °C es marcada como anomalía

---

## US-08: Exportación de historial de lecturas a CSV
**Como** analista de datos,  
**quiero** exportar el historial de lecturas a un archivo `.csv`,  
**para** procesar las mediciones en herramientas externas como Excel o Python.

### Scenario: Generación exitosa de archivo CSV
- **Given** que existen 10 lecturas guardadas para el sensor "TEMP-01"
- **When** ejecuto la acción de exportación a "reporte.csv"
- **Then** se genera un archivo CSV válido con 10 filas de datos y cabeceras correctas

---

## US-09: Simulación de red de sensores (Gaussian Simulator)
**Como** desarrollador de software,  
**quiero** generar un simulador con distribución gaussiana para 10 sensores concurrentes,  
**para** realizar pruebas de carga y estrés en el sistema.

### Scenario: Generación de datos sintéticos de prueba
- **Given** un simulador configurado con media de 25.0 °C y desviación estándar de 2.0
- **When** ejecuto una simulación de 60 ciclos de lectura
- **Then** se devuelven 60 lecturas válidas dentro del rango probabilístico esperado

---

## US-10: Limpieza y purga de lecturas antiguas
**Como** administrador del sistema,  
**quiero** purgar lecturas con una antigüedad mayor a 30 días,  
**para** optimizar el uso de almacenamiento y la velocidad de consulta.

### Scenario: Purga de datos fuera de retención
- **Given** registros de lecturas almacenados hace más de 30 días
- **When** se ejecuta el proceso de mantenimiento nocturno
- **Then** las lecturas antiguas son eliminadas permanentemente del almacenamiento