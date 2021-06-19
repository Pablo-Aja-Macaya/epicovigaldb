# -*- coding: utf-8 -*-
## Celery file
from epicovigal.celery import app
import glob

######################
# Ejecución de tests #
from .test_execution import *

@app.task
def execute_command(cmd, execute_from_here=TESTS_OUTPUT_TMP):
    # Ejecución de test
    p = subprocess.call(cmd, cwd=execute_from_here, shell=True)
    # Comando para limpiar archivos temporales
    p = subprocess.call('rm ./*', cwd=execute_from_here, shell=True)




