## Aquí se explica que correcciones se tomaron y el por qué

## **m_reading.py**
 
La IA me hizo ver que había errores relacionados con el límite de los valores y sus unidades, lo que puede desencadenar en errores cruciales en la base de datos, de igual forma, la longitud de los datos y poca documentación para el tiempo no permite un trabajo totalmente acertado.

Menciona acerca de un desacoplamiento de reglas de validación del dominio, aunque corregir esto puede llevar a errores con la lógica, por lo que se optará por arreglarse más tarde.


## **m_sensor.py**

La IA encontró entre las cosas más criticas una falta de validación de SOLID, siendo Single Responsibility en min_value y max_value, se está considerando arreglar dicho error y aceptar la resolución propuesta por Copilot.

Hay más errores de seguridad, y quitando al de init__ explícito, se buscarán o aceptaran las propuestas dadas por copilot.

## **reading_repo.py**

De nueva cuenta SOLID está comprometido en este código con Single Responsibility, siendo get_by_sensor() el del error, no se aceptará como tal la propuesta pero si se considerará para una futura solución.

Me marcó nuevos casos borde en la misma función, asímismo en from_date > to_date, siendo portenciales riesgos, se aceptará la propuesta descrita.

También hay un riesgo de seguridad potencial en create(), lo que puede exponer detalles internos de la API, se aceptó la propuesta dada.


## **sensor_repo.py**

Otro error más de SOLID, siendo esta vez Dependency inversion, siendo la clase lo que dificulta hacer testeos ya que depende totalmente de SQALchemy, se aceptará la propuesta.

De nueva cuenta casos borde sin ser manejados así como de seguridad en diversas lineas del programa, se corregiran acorde a lo propuesto por copilot.