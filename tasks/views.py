from django.shortcuts import render
from .models import Task
#from django.contrib.auth.decorators import login_required
from upload.models import Sample
from .models import Team, Team_Component
from tests.models import NextcladeTest, LineagesTest
from upload.models import SampleMetaData
from reports.models import Report
from reports.ayudantes import get_report_urls

#@login_required(login_url="/accounts/login")
def home(request):
    sample_count = Sample.objects.filter(id_uvigo__contains='EPI').exclude(id_uvigo__contains='ICVS').count()
    sequenced_count = SampleMetaData.objects.exclude(fecha_entrada_fastq__isnull=True).exclude(id_hospital='ICVS').exclude(id_uvigo_id__id_uvigo__contains='SERGAS').count()
    lineage_count = LineagesTest.objects.exclude(id_uvigo_id__id_uvigo__contains='SERGAS').exclude(id_uvigo_id__id_uvigo__contains='ICVS').values('lineage').distinct().count()
    report = None
    urls_dicc = None
    if request.user.is_authenticated:
        tasks = Task.objects
        url = 'tasks/home.html'
    else:
        tasks = Task.objects.filter(show_to='all')
        url = 'tasks/visitor_home.html'
        try:
            data = Report.objects.filter(tipo='mensual').order_by('-fecha_inicial')
            report = data[0]
            urls_dicc = get_report_urls(report)
        except:
            # la entrada no existe en la base de datos
            report = None
            urls_dicc = None

    context = {
        'tasks':tasks, 
        'sample_count':sample_count, 
        'sequenced_count':sequenced_count, 
        'lineage_count':lineage_count
        }
    if report:
        context['data'] = data
    if urls_dicc:
        context = {**context, **urls_dicc}

    return render(request, url, context)

def consorcio(request):    
    dicc = {}
    for t in Team.objects.all().order_by('id_team'):
        dicc[t] = Team_Component.objects.filter(id_team=t).order_by('person')
    url = 'tasks/consorcio.html'
    return render(request, url, {'teams':dicc})

