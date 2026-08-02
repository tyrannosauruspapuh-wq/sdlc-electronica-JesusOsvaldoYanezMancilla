# 3. Arquitectura en Capas e Inyección de Dependencias para la API de SensorHub

* **Estado:** Aceptado
* **Fecha:** 2026-07-31
* **Autor:** Jesús Osvaldo Yáñez Mancilla

## Contexto
A medida que la API de SensorHub crece en complejidad con CRUDs de sensores, validaciones de rangos físicos y operaciones de base de datos, mezclar la lógica de negocio, las consultas a la base de datos y los manejadores de rutas en un solo archivo (ej. `main.py`) genera un código acoplado, difícil de mantener y casi imposible de probar con pruebas unitarias/integración aisladas. Se requiere establecer una separación clara de responsabilidades en la arquitectura de software.

## Decisión
Hemos decidido implementar una **arquitectura de 4 capas limpiamente separadas** utilizando el patrón de **Inyección de Dependencias (DIP)** nativo de FastAPI y SQLAlchemy 2.0:

1. **Capa de Dominio/Esquemas (`schemas/`):** Modelos de Pydantic v2 que definen los contratos de entrada/salida y validaciones estrictas (ej. rangos de temperatura/humedad).
2. **Capa de Persistencia (`models/` y `database.py`):** Modelos ORM de SQLAlchemy 2.0 (`DeclarativeBase`) que mapean las tablas en SQLite/PostgreSQL y gestionan el ciclo de vida de las sesiones (`get_db`).
3. **Capa de Repositorio/Servicio (`services/`):** Clases o funciones encargas de la lógica de negocio y las consultas ORM puras, desacopladas del framework web.
4. **Capa de Entrada/Rutas (`routers/`):** Endpoints de FastAPI (`APIRouter`) encargados únicamente del ruteo HTTP, la deserialización de peticiones, la invocación de servicios y el retorno de respuestas semánticas.

Para desacoplar la base de datos durante el testing, las sesiones se inyectan a los routers mediante `Depends(get_db)`.

## Alternativas consideradas
* **Lógica de negocio y consultas directas en las rutas (Fat Routers):** Se descartó porque violaba el Principio de Responsabilidad Única (SRP), dificultando la reutilización de código y haciendo los tests dependientes de una base de datos de desarrollo activa.
* **Uso de un ORM asíncrono (Tortoise / SQLModel):** Se descartó para mantener simplicidad en SQLite local durante esta fase y asegurar el uso de la sintaxis estándar moderna de **SQLAlchemy 2.0 + Alembic** requerida por el programa.

## Consecuencias
* **Positivas:** 
  * **Alta testeabilidad:** Permite sobreescribir la dependencia `get_db` en `pytest` usando `app.dependency_overrides` para ejecutar pruebas sobre una base de datos SQLite en memoria (`sqlite:///:memory:`).
  * **Mantenibilidad:** Modificar una validación física o una consulta SQL no altera los controladores HTTP ni rompe los contratos OpenAPI.
  * **Alineación SOLID:** Cumple estrictamente con SRP (Single Responsibility) y DIP (Dependency Inversion Principle).
* **Negativas / Limitaciones:**
  * Incrementa la cantidad de archivos iniciales en la estructura del proyecto (`routers/`, `services/`, `models/`, `schemas/`).
  * Requiere un entendimiento claro de cómo fluyen los datos entre objetos Pydantic, entidades SQLAlchemy y el generador de contexto de sesiones.