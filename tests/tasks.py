# -*- coding: utf-8 -*-
## Celery file
from epicovigal.celery import app
import glob

@app.task
def check_status():
    print('CHECKING STATUS...')
    print(len(glob.glob("/home/pabs/GitRepos/EPICOVIGAL/BD_input_files/*_lineages.csv")))
    # name = 'EPI.CHOP.201_lineages.csv'.split('_lineages.csv')

