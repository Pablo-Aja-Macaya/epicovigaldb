from django.shortcuts import render
from .models import Task
#from django.contrib.auth.decorators import login_required
from upload.models import Sample
from .models import Team, Team_Component
from tests.models import NextcladeTest, LineagesTest
from upload.models import SampleMetaData

def read_log():
    with open('/home/pabs/MasterBioinformatica/TFM/prueba_log_.txt','rt') as log:
        lista = []
        for line in log:
            dicc = eval(line)
            print(dicc)
            lista.append(dicc)
    return lista
# In [57]: with open(file, 'wt') as log:
#     ...:     try:
#     ...:         int('p')
#     ...:     except Exception as e:
#     ...:         dicc = {
#     ...:             'archivo':'EPI.BLABLA.200',
#     ...:             'error':e,
#     ...:             'traceback':str(traceback.format_exc()).replace('"',' ').replace("'", ' ')
#     ...:         }
#     ...:         log.write(str(dicc))

#@login_required(login_url="/accounts/login")
def home(request):
    sample_count = Sample.objects.all().count()
    sequenced_count = SampleMetaData.objects.exclude(fecha_entrada_fastq__isnull=True).count()
    #clade_count = NextcladeTest.objects.values('clade').distinct().count()
    lineage_count = LineagesTest.objects.values('lineage').distinct().count()
    if request.user.is_authenticated:
        tasks = Task.objects
        url = 'tasks/home.html'
    else:
        tasks = Task.objects.filter(show_to='all')
        url = 'tasks/visitor_home.html'
    context = {'tasks':tasks, 'sample_count':sample_count, 'sequenced_count':sequenced_count, 'lineage_count':lineage_count, 'log':read_log()}
    return render(request, url, context)

def consorcio(request):    
    dicc = {}
    for t in Team.objects.all().order_by('id_team'):
        dicc[t] = Team_Component.objects.filter(id_team=t).order_by('person')
    url = 'tasks/consorcio.html'
    return render(request, url, {'teams':dicc})

