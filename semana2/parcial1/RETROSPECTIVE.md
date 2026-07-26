# Sprint Retrospective — Evaluación 1

**Fecha:**26 de Julio 2026  
**Proyecto:** SensorHub  
**Autor:** Jesús Osvaldo Yáñez Mancilla  

---

## Lo que salió bien: 
1. **Implemetación de TDD:** Escribir los tests unitarios antes que la lógica principal en `SensorReading`, `AnomalyDetector` y `AlertManager` ayudó a diseñar interfaces más limpias y predecir casos borde desde el inicio.
2. **Cumplimiento de herramientas de calidad:** La integración temprana de `ruff` y `mypy` permitió mantener el código sin violaciones de estilo PEP 8 ni errores de tipado estático antes de cada commit.
3. **Uso del Patrón Estrategia:** La separación de `AlertStrategy` en implementaciones concretas (`ConsoleAlert` y `FileAlert`) permitió cumplir con el principio de Abierto/Cerrado (OCP).

---

## Cosas a mejorar:
1. **Manejo de rutas y estructuras de módulos en Python:** Inicialmente ocurrieron pequeños conflictos de resolución con `mypy` y `pytest` al organizar las carpetas de la `semana2`, los cuales se resolvieron añadiendo correctamente los archivos `__init__.py`.
2. **Estimación inicial de tareas:** La configuración de herramientas de calidad y el ajuste fino de la cobertura de código requerida ($\ge 80\%$) tomaron un poco más de tiempo de lo previsto respecto al desarrollo puro de las funcionalidades.
3. **Uso correcto de ramas en Github:** Al momento de trabajar en esta semana se olvidó por completo hacer una rama distinta a la Main en el repositorio, si bien no afecta en nada al funcionamiento, para futuras fases se considerará dicho error buscando la correcta implementación de las herramientas disponibles.
---

## Acción concreta para el siguiente Sprint
* **Implementar pre-commit hooks:** Configurar `pre-commit` localmente para que valide automáticamente `ruff check` y `mypy` antes de cada commit, evitando sorpresas de linter o tipado al correr los pipelines de integración continua, esto con el fin de mejorar todo el proceso de la documentación y demás.