# Instalación de epicovigaldb

Esta aplicación usa: Ubuntu, Django, Pyhton, Gunicorn, Celery, Redis, Supervisor y una base de datos (MySQL). Para que todas las funciones estén activas son necesarias todas menos Supervisor. Para ver la web pero sin usar la cola de tareas (no se podrán actualizar los datos) sólo es necesario Django, Python y MySQL. 

En primer lugar, se obtiene el código:
```
git clone https://github.com/Pablo-Aja-Macaya/epicovigaldb
```

La aplicación usa un entorno virtual creado con `virtualenv`:
```
cd /path/for/env
virtualenv django
```

Activar entorno:
```
source /path/to/env/bin/activate
```

Una vez creado, usar el archivo `pip_requirements.txt`para instalar todas las carpetas:
```
pip install -r pip_requirements.txt
```

#### Falta instalar celery, mysql, redis, gunicorn

Una vez MySQL esté instalado y configurado, se importa un dump de la base de datos:
```
FALTA
```

# Manejo de epicovigaldb en local

Cualquier cambio que se haga en código se debe probar primero en la instalación local, **nunca** en el servidor. A continuación se explicará el sistema de Django y ciertos elementos de la herramienta. Para "encenderla" en local se usa:
```
python manage.py runserver
```
La herramienta epicovigaldb está compuesta de varias "aplicaciones" o partes. Por ejemplo, la subida de metadatos clínicos se encuentra en la carpeta `upload/`. 

En cada aplicación se encuentran varios archivos básicos importantes: `views.py`, `models.py`, `urls.py` y los `templates`. También peude haber `forms.py`, las cuales contienen formularios.

## URLs y Views
En `urls.py` se encuentran las URLs de la aplicación, que especifican la función de `views.py` a la que dirigir al usuario. Las funciones de `views.py` son las que llevan al usuario de una página a otra, y son las que envían o reciben variables de los HTML.

## Models
El archivo `models.py` define las tablas de la aplicación. Por ejemplo, en upload/models.py se encuentran las tablasd de metadatos de la base de datos. Cada atributo de un modelo define sus características (longitud, tipo, llave primaria...). La base de datos se crea a partir de estos modelos, y cualquier modificación importante **debe** hacerse desde el código de la herramienta. Si, por ejemplo, se borrase una columna directamente desde SQL se producirían problemas, ya que la herramienta esperará esa columna, y como no la hay, dará error y no funcionará. Cambios como borrar entradas de una tabla sí se pueden hacer.

Cuando se modifica, crea o elimina un modelo de `models.py` es necesario hacer migraciones a la base de datos (sincronizar la herramienta y la base de datos). Para ello, cerrar la herramienta (ctrl+C en terminal) y:
```
python manage.py makemigrations
python manage.py migrate
```

### Añadir atributo a tabla de muestras
Si, por ejemplo, si se quisiese añadir un atributo a la tabla Samples de `upload/models.py`, lo único que habría que hacer sería:
- Añadir línea con nombre y características del atributo al modelo.
- Migrar la base de datos (`makemigrations` y `migrate`)

Una vez hecho esto, es necesario añadirla a las funciones de subida de datos. En `upload/utils/upload_utils.py`, alrededor de las líneas 152-184, se encuentra la correspondencia entre el código que aparece en los excels del proyecto (llave) y los de la base de datos (valor). En este diccionario se añade el nuevo campo, con su nombre original a la izquierda y el nombre en la base de datos a la derecha (el que se ha puesto en `models.py`). 

Tras esto, añadir la lectura de la variable entre las líneas 211-230, siguiendo el formato del resto. Puede ser necesario modificar el valor a mayores si: es un float que puede tener punto o coma (líneas 232-236), es un float que a veces puede estar en blanco (check_numbers en 238-242) una fecha con formatos varios (time_transform en 258-265).

El último paso es añadir la variable entre las líneas 278-338 para que se inserte en la base de datos. En este apartado hay varios update_or_create, meter la variable en la tabla que corresponda con el mismo formato que el resto de atributos.

Si se quisiese retirar un atributo habría que hacer los mismos pasos pero al revés, acabando quitando su definición en `models.py` y realizando las migraciones.

### Añadir atributo a tabla de test
En `tests/` se localizan las funciones relacionadas con la parte de herramientas bioinformáticas. En `models.py` se encuentran las definiciones de las tablas, y en `subidas_tests.py`se realiza la subida de esta información.

Para añadir una nueva columna a una tabla se realizan pasos similares al anterior apartado:
- Añadir línea con nombre y características del atributo al modelo.
- Migrar la base de datos (`makemigrations` y `migrate`)
- Añadir el atributo al diccionario entre las líneas 16-84 para la tabla específica. Las llaves son los nombres originales y los valores son los nombres en la base de datos. Poner todo en minúscula.

Cada test tiene una función propia. Por ejemplo, para Picard, sólo sería necesario modificar `upload_picard` (165-188), recogiendo el atributo de cada línea en el archivo y añadiéndolo en el update_or_create con el mismo formato que el resto.

El único test distinto es el de iVar (`upload_variants`, 276-346). Para estos archivos se usa un bulk_update o bulk_create porque tienen muchas más líneas por archivo. Hay que coger el atributo entre las líneas 288-298 y ponerlo tanto en 301-318 como en 320-335, con el formato que tengan el resto de atributos en estas zonas. Por último, hay que añadir a la línea 342 (`update_fields`) el nuevo atributo.

## Gráficas
La gráficas vienen dadas por la aplicación `visualize` y se encuentran al fondo de `views.py`. Cada gráfica tiene su propio URL, al que se llama desde el HTML. En el caso de https://epicovigaldb.com/visualize/graphs/ el funcionamiento es el siguiente:
- Cuando se llama a su URL el views `get_graphs` comprueba si se le ha enviado un formulario (request.method=='POST'), como todavía no se cumple, la función devuelve la página con el formulario vacío.
- El usuario selecciona los campos del formulario y lo envía.
- Ahora el views usa la información del formulario y crea un código en base64 con este, que contendrá la información del formulario. 
- Tras esto, el views devuelve al usuario a la página, llevando en el contexto las URLs de las gráficas.
- Una vez en el HTML (`visualize/templates/visualize/graphs.html`), existen apartados donde se pondrá cada gráfica.
- El apartado con el URL {{url_linajes_hospital}} es llamado por una función de ajax (fondo de la página). Cada gráfica tiene su propio views y reciben el diccionario en base64 con los atributos seleccionados. Tras esto, filtra y devuelve el JSON, que la librería Highcharts se encarga de traducir a gráfica.


# Manejo de epicovigaldb en servidor
Una vez se han probado los cambios hechos en local, se hace un push a Git para subirlo a esta carpeta. El siguiente paso es conectarse al servidor y, una vez dentro, ir a la carpeta `epicovigal/epicovigaldb`. Desde aquí se hace un `git pull`. Si los cambios incluyen migraciones es necesario activar el entorno virtual de la aplicación y realizarlas:
```
source ../django/bin/activate
python manage.py makemigrations
python manage.py migrate
```
Para que los cambios tengan efecto, hay que reiniciar Gunicorn, Redis y Celery (Supervisor). Ejecutar lo siguiente 2 veces:
```
sudo systmctl restart gunicorn
sudo systemctl restart redis
sudo supervisorctl restart all
```



