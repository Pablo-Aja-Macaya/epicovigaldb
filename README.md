# Aplicación
La aplicación consiste en el manejo de la base de datos del proyecto EPICOVIGAL, ejecución de herramientas bioinformáticas y actualización automática de datos. Puede verse en:
- [Ver parte abierta](https://epicovigaldb.com)

# Instalación de epicovigaldb

Esta aplicación usa: Ubuntu, Django, Pyhton, Gunicorn, Celery, Redis, Supervisor y una base de datos (MySQL). Para que todas las funciones estén activas son necesarias todas menos Supervisor. Para ver la web pero sin usar la cola de tareas (no se podrán actualizar los datos) sólo es necesario Django, Python y MySQL.

En primer lugar, se obtiene el código:
```
git clone https://github.com/Pablo-Aja-Macaya/epicovigaldb
```
## Instalar base de datos
La aplicación usa MySQL (aunque en teoría podría usar cualquier base de datos). Para instalarlo:
```
sudo apt install mysql-server
```

## Entorno virtual
Se usa un entorno virtual creado con `virtualenv`. La aplicación sólo podrá funcionar desde un terminal que esté en el entorno. Para instalar virtualenv:
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
```
Para crear el entorno virtual:
```
cd /path/for/env
virtualenv django
```

Ahora hay que meterse en el entorno con:
```
source django/bin/activate
```

E instalar todos los paquetes necesarios con el archivo `epicovigaldb/pip_requirements.txt`:
```
sudo apt install libmysqlclient-dev
pip install -r ./epicovigaldb/pip_requirements.txt
```

Activar entorno:
```
source /path/to/env/bin/activate
```
## Configurar base de datos

Entrar en MySQL y crear la base de datos:
```
sudo mysql -u root
CREATE DATABASE epicovigal_web;
```

Configurar un usuario que tenga acceso a esta y sólo esta (si se usa root hay problemas de seguridad, ya que root puede acceder a todas las bases de datos):
```
CREATE USER 'nombre_usuario'@'%' IDENTIFIED WITH mysql_native_password BY 'contraseña';
GRANT ALL ON epicovigal_web.* TO 'nombre_usuario'@'%';
FLUSH PRIVILEGES;
```

Una vez MySQL esté instalado y configurado, se importa un dump de la base de datos (pedir a administrador):
```
sudo mysql -u root -p epicovigal_web < dump.sql
```

## Configuración local

Ahora es necesario crear un archivo de configuración local en `epicovigaldb/epicovigal/local_settings.py`. **Este archivo jamás debe subirse a GitHub, ya que va a tener información peligrosa**. También contendrá caminos relativos al sistema en el que se use la aplicación. Esta configuración será importada por `epicovigdaldb/epicovigal/settings.py`. 

En este archivo se meten las credenciales a la base de datos:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'epicovigal_web',
        'USER': 'nombre_usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

La llave secreta (importante que no se filtre) también va en este archivo. Se genera una vez con:
```
from django.core.management.utils import get_random_secret_key  
get_random_secret_key()
```
Y se pone en `epicovigaldb/epicovigal/local_settings.py` como:
```
SECRET_KEY = 'resultado de la función anterior'
```

Otra configuración importante es especificar el estado de la aplicación. Las siguientes líneas se usan en el servidor cuando la web está activa, ya que si esta da error no revelará datos y variables importantes. Lo más importante es que en el servidor `DEBUG = TEMPLATE_DEBUG = False`, pero en local esto es mejor si es `DEBUG = TEMPLATE_DEBUG = True` para poder encontrar los fallos en el desarrollo.
```
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
DEBUG = TEMPLATE_DEBUG = False
SECURE_SSL_REDIRECT = True
```

También se pone:
```
GS_DATA_KEY = 'pedir llave'
GS_DATA_GID = 'pedir llave'
GS_DATA_GID_LIST = ['pedir llave','pedir llave']

ALLOWED_HOSTS = ['193.144.35.166','epicovigaldb.com','www.epicovigaldb.com']

# Caminos para actualizar desde carpeta en tests
TESTS_PCKL_FOLDER = '/root/epicovigal/data/' # camino de la caché
TESTS_FOLDER_BASE = '/mnt/epicovigal/data/'

# Esto obtiene ip de la gente que accede al login
AXES_META_PRECEDENCE_ORDER = [
   'HTTP_X_FORWARDED_FOR',
   'REMOTE_ADDR',
]
```

## Configuraciones adicionales
Debido a problemas en una de las migraciones con respecto al servidor falta `epicovigaldb/tests/migrations/0070_country_lineagestest.py`. Pedir al administrador y sólo copiar el archivo en `epicovigaldb/tests/migrations/`.

Una vez que la base de datos ha sido creada e importada, y Django tiene acceso a ella, es necesario aplicar migraciones (sincronizar Django con la base de datos):
```
python manage.py makemigrations
python manage.py migrate
```
Y crear un superuser:
```
crear superuser
```
Probar que funciona con:
```
python manage.py runserver
```

## Celery, Redis, Gunicorn y Supervisor

Para realizar tareas asíncronas se usan Celery y Redis. Con `pip install -r epicovigaldb/pip_requirements.txt` ya se instala casi todo, únicamente falta instalar Redis:

```
sudo apt install redis-server
```
Para que funcione la actualización desde el Google Sheet, la actualización por carpetas o la actualización de coordenadas es necesario que estén activos. En local, se puede simplemente iniciar en tres terminales separadas cada parte. Primero Django, luego Redis y después Celery:

```
python manage.py runserver # ventana 1
sudo systemctl restart redis # ventana 2
celery -A epicovigal worker # ventana 3
```

En el servidor se usan estas tres partes (Django, Celery y Redis) junto a Gunicorn. Gunicorn es el que activa la aplicación de Django en un entorno virtual indicado. En el servidor se encuentran automatiadas, de tal manera que cuando se recibe una petición automáticamente se activan todas las partes. Para una instalación local no es necesario. 

La automatización se da de la siguiente manera: el servidor recibe una petición mediante NGINX, este despierta a Gunicorn, el cual despierta a Django. Redis está siempre activo y Celery está manejado por Supervisor, siempre activo.

## NGINX
El servidor usa NGINX para manejar las peticiones online a la herramienta, pero en local no es necesario.

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

Una vez hecho esto, es necesario añadirla a las funciones de subida de datos. En `upload/utils/upload_utils.py`, alrededor de las líneas [152-184](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/upload/utils/upload_utils.py#L152-L184), se encuentra la correspondencia entre el código que aparece en los excels del proyecto (llave) y los de la base de datos (valor). En este diccionario se añade el nuevo campo, con su nombre original a la izquierda y el nombre en la base de datos a la derecha (el que se ha puesto en `models.py`). 

Tras esto, añadir la lectura de la variable entre las líneas [211-230](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/upload/utils/upload_utils.py#L211-L229), siguiendo el formato del resto. Puede ser necesario modificar el valor a mayores si: es un float que puede tener punto o coma (líneas [232-236](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/upload/utils/upload_utils.py#L232-L236)), es un float que a veces puede estar en blanco (check_numbers en [238-242](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/upload/utils/upload_utils.py#L238-L242)) una fecha con formatos varios (time_transform en [258-265](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/upload/utils/upload_utils.py#L258-L265)).

El último paso es añadir la variable entre las líneas [278-338](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/upload/utils/upload_utils.py#L278-L337) para que se inserte en la base de datos. En este apartado hay varios update_or_create, meter la variable en la tabla que corresponda con el mismo formato que el resto de atributos.

Si se quisiese retirar un atributo habría que hacer los mismos pasos pero al revés, acabando quitando su definición en `models.py` y realizando las migraciones.

### Añadir atributo a tabla de test
En `tests/` se localizan las funciones relacionadas con la parte de herramientas bioinformáticas. En `models.py` se encuentran las definiciones de las tablas, y en `subidas_tests.py`se realiza la subida de esta información.

Para añadir una nueva columna a una tabla se realizan pasos similares al anterior apartado:
- Añadir línea con nombre y características del atributo al modelo.
- Migrar la base de datos (`makemigrations` y `migrate`)
- Añadir el atributo al diccionario entre las líneas [16-84](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L16-L85) para la tabla específica. Las llaves son los nombres originales y los valores son los nombres en la base de datos. Poner todo en minúscula.

Cada test tiene una función propia. Por ejemplo, para Picard, sólo sería necesario modificar `upload_picard` ([165-188](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L165-L188)), recogiendo el atributo de cada línea en el archivo y añadiéndolo en el update_or_create con el mismo formato que el resto.

El único test distinto es el de iVar (`upload_variants`, [276-346](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L276-L346)). Para estos archivos se usa un bulk_update o bulk_create porque tienen muchas más líneas por archivo. Hay que coger el atributo entre las líneas [288-298](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L288-L298) y ponerlo tanto en [301-318](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L301-L318) como en [320-335](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L319-L335), con el formato que tengan el resto de atributos en estas zonas. Por último, hay que añadir a la línea [342](https://github.com/Pablo-Aja-Macaya/epicovigaldb/blob/6589725e9ea35993be7c0bcb32af1589f4f016c7/tests/subida_tests.py#L342) (`update_fields`) el nuevo atributo.

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

Nota: En realidad si no se han cambiado funciones que usen Celery y Redis sólo es necesario hacerlo para Gunicorn, pero es mejor asegurarse.

Si se está dentro del entorno virtual, se puede acceder a la consola de Django con:
```
python manage.py shell
```
Y a la base de datos sin que te pida credenciales (ya las tiene Django en la configuración local) con:
```
python manage.py dbshell
```



