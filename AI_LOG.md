# Semana 1 

## Entrada 1: 

**Prompt: "Dame 1 ejercicio en el que me pueda basar para entender la sig. actividad: Ejercicio: escribe 5 funciones puras sobre Reading (conversión de unidades, detección de umbral, serialización) con type hints completos;"**

La IA me propuso un ejercicio en el cual se usaban los grados de temperatura, acepte dicha ayuda y me base en conceptos similares para los demás ejercicios.



# Semana 2

## Entrada 1:
 **Prompt: ¿Puedes ayudarme con las actividades del día martes? aún no entiendo del todo esto de los user stories y de Gherkin, asímismo, puedes darme ejemplos de las user stories siguiendo el panorama del sensor y sus lecturas, gracias!**

 La IA me explico de forma un poco más clara para mi lo que le pedí hacerca de las user stories y Gherkin, también me dio los ejemplos de los US que necesitaba, ya con todo eso claro, me prpuse a modificar dichos ejemplos a una mejor manera.

## Entrada 2:

**Prompt: Ayudame a verificar mis User Stories, revisa lo siguiente: “¿es verificable? ¿es ambiguo? ¿qué caso borde falta?”, !gracias!**

Revise lo que me dio la IA que revisara, ya que algunos escenarios no los había considerado de forma adecuada ante el proyecto.

## Entrada 3:
Para este prompt pedí ayuda con lo relacionado a la TDD, ya que aún no tenía muy en claro lo que debía de hacer

**Prompt: En base a la actividad del día miércoles, ¿puedes ayudarme a realizarla? aún no tengo muy claro que debo de hacer y como lo debo de, de igual forma no tengo aún claro un código para implementra, entoces si pudieras darme un ejemplo de código sería también asombroso, ¡gracias!**

La IA me explicó como hacer las actividades, al final fueron más fáciles de lo que yo esperaba, aunque de igual forma investigue por mi cuenta cuestiones como los comandos de git en VS, aquí estuve familiarizandome con la interfaz de VS ya que nunca la había usado de tal manera, en cuanto al código de ejemplo y los commits que debía de hacer, no use el que me dió la IA como tal, pero sí lo tome como referencia para poder prácticar por mi cuenta la programación.

## Entrada 4:
Ahora pasé a la parte del día jueves, debido a que no sabia como configurar pyproject.toml le pedi ayuda de manera similar al día anterior a la IA:

**Prompt: Ahora pasando a las actividades del día jueves, ¿cómo se configura el pyproject.toml? la verdad si le tengo miedo porque nunca había escuchado de esto jajaja, si se me hace algo complicado.**

Lo que me dió la Ia fue una guía de los conceptos que se mencionan en la actividad a cumplir, así como un código para pyproject.toml, si bien el código me servía, busqué en otras fuentes códigos similares o que cumplieran la función pedida para tener una referencia y así  corregir algún error en caso de ser necesario.

## Entrada 5:
En las actividades del día viernes tuve complicaciones, primero con mypy y ruff, por lo que le pedí a la IA que analizará los errores:

**Prompt: ¿Puedes verificar que salió mal con este código? aún no estoy muy familiarizado con mypy y ruff y la verdad que no sé que significa cada cosa jajaja.**

Lo que me dió la IA fue una guía para corregir los errores, resulta que era muy sencillo y yo me estaba complicando la vida, aún asi busque en la fuente de ruff los errores asi como los de mypy y los fui corrigiendo uno por uno, algo tardado si, pero era necesario.

## Entrada 6:
Aquí fue más de pánico jajaja, lo que pasa es que olvidé por completo hacer otras ramas para la semana, al estar viendo conceptos nuevos mis prioridades se fueron a entender eso y dejar de lado las buenas prácticas de git, al momento de terminar el TDD del viernes es cuando me dí cuenta, aunque ya prácticamente había acabado todo.

**Prompt: Oye es que pasó algo, dígamos que olvidé hacer otras ramas para el repositorio mientras trabajaba en esta semana, ¿me recomiendas borrar todo y empezar de nuevo o ya terminar todo así como esta? lol.**

La IA me convenció de no hacer todo de nuevo (ya estoy pasado de tiempo de entrega al momento de escribir esto) y de simplemente recordar hacer todo al inicio de cada semana y actividad si es considerable.


# Semana 3

## Entrada 1:
Al definir los modelos de Pydantic para los sensores, quería validar que las lecturas no estuvieran fuera de los rangos físicos reales (ej. temperaturas negativas imposibles para ciertos sensores).

**Prompt:** "Ayúdame a hacer un validator en Pydantic v2 para que rechace temperaturas menores a -273.15 °C o mayores a 1000 °C en el esquema de SensorCreate."

La IA sugirió usar `@field_validator` de Pydantic v2. Acepté la sugerencia del decorador, pero ajusté la lógica para que los límites dependieran dinámicamente del `sensor_type` (temperatura, humedad, presión) en lugar de un rango global quemado en código.

---

## Entrada 2:
Estaba teniendo un enredo configurando SQLAlchemy 2.0 y la sesión asíncrona/síncrona con SQLite para los endpoints CRUD.

**Prompt:** "Dame el boilerplate de database.py para SQLAlchemy 2.0 con SQLite usando sessionmaker y declarative_base."

La IA me dio una configuración funcional, pero estaba mezclando sintaxis vieja de SQLAlchemy 1.4 (`declarative_base()`) con la nueva sintaxis 2.0 (`DeclarativeBase`). Rechacé la sintaxis heredada y reescribí la clase base usando `class Base(DeclarativeBase): pass` para mantener el estándar moderno que pide el programa.

---

## Entrada 3:
Al integrar Alembic para gestionar las migraciones de la base de datos de SensorHub, los comandos iniciales me estaban fallando porque no detectaba los modelos.

**Prompt:** "Alembic revision --autogenerate no detecta mis tablas en env.py, ¿qué me falta importar?"

La IA identificó correctamente que en `env.py` faltaba importar la `Base` de mis modelos y asignar `target_metadata = Base.metadata`. Apliqué el cambio directo y pude generar la migración `init_db` sin problemas.

---

## Entrada 4:
Para cumplir con el coverage de tests (>= 80%), necesitaba probar las rutas HTTP de FastAPI usando `TestClient` e `httpx`, pero no quería que los tests modificaran la base de datos local.

**Prompt:** "¿Cómo puedo hacer un fixture de pytest en FastAPI para que use una base de datos SQLite en memoria (sqlite:///:memory:) durante las pruebas?"

La IA propuso una fixture de `pytest` que sobreescribe la dependencia `get_db` usando `app.dependency_overrides`. Acepté la estrategia porque aísla completamente las pruebas sin tocar la base de datos de desarrollo.

---

## Entrada 5:
Necesitaba documentar bien los códigos de respuesta HTTP en FastAPI para que Swagger (`/docs`) se viera impecable para la revisión.

**Prompt:** "¿Cómo agrego respuestas de error personalizadas (ej. 404 Not Found) con esquemas en la decoración de una ruta de FastAPI para que aparezcan en Swagger?"

La IA me sugirió usar el parámetro `responses={404: {"description": "Sensor no encontrado"}}` en los decoradores de los endpoints. Lo apliqué en los endpoints de `GET /sensors/{id}` y `DELETE /sensors/{id}` para dejar la documentación clara para mi revisor de pares.

---

## Entrada 6:
Aquí fue más de pánico jajaja, lo que pasa es que olvidé por completo hacer un PR y no estaba seguro de que hacer.

**Prompt:** "Oye es que pasó algo, dígamos que olvidé hacer el PR en guthub jajaja, me ayudas a tener todo listo?

La IA me dió instrucciones de cómo realizar todo, resulta que era más sencillo de lo que pensaba, además de ya conocer el método.