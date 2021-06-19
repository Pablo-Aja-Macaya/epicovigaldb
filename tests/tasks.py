# -*- coding: utf-8 -*-
## Celery file
from epicovigal.celery import app
import glob

######################
# Ejecución de tests #
from .test_execution import *

@app.task
def execute_command(files, cmd_function, execute_from_here=TESTS_OUTPUT_TMP):
    cmd_function = CMD_FUNCTION_DICT[cmd_function]
    for i in files:
        # Ejecución de test
        cmd = cmd_function(i)
        p = subprocess.call(cmd, i, cwd=execute_from_here, shell=True)
        # Comando para limpiar archivos temporales
        p = subprocess.call('rm ./*', cwd=execute_from_here, shell=True)


