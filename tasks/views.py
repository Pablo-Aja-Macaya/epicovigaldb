from django.shortcuts import render
from .models import Task
#from django.contrib.auth.decorators import login_required
from upload.models import Sample
from .models import Team, Team_Component
from tests.models import NextcladeTest


#@login_required(login_url="/accounts/login")
def home(request):
    sample_count = Sample.objects.all().count()
    sequenced_count = SampleMetaData.objects.exclude(fecha_entrada_fastq__isnull=True).count()
    clade_count = NextcladeTest.objects.values('clade').distinct().count()
    if request.user.is_authenticated:
        tasks = Task.objects
        url = 'tasks/home.html'
    else:
        tasks = Task.objects.filter(show_to='all')
        url = 'tasks/visitor_home.html'
    context = {'tasks':tasks, 'sample_count':sample_count, 'sequenced_count':sequenced_count, 'clade_count':clade_count}
    return render(request, url, context)

def consorcio(request):    
    dicc = {}
    for t in Team.objects.all().order_by('id_team'):
        dicc[t] = Team_Component.objects.filter(id_team=t).order_by('person')
    url = 'tasks/consorcio.html'
    return render(request, url, {'teams':dicc})

##############
## Gráficas ##
from upload.models import SampleMetaData
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Count
from datetime import date, datetime
import geojson
import random

def concellos_gal_graph(request, fecha_inicial, fecha_final):
    map_file = '/home/pabs/GaliciaConcellos_Simple.geojson'
    # map_file = '/home/pabs/GaliciaComarcas.geojson'
    with open(map_file) as map:
        geojson_data = geojson.load(map) # mapa


    # data = list(Sample.objects.values('id_region__localizacion').filter(id_region__localizacion__gte=2).order_by().annotate(NomeMAY = F('id_region__localizacion') , value=Count('id_region__localizacion')))
    
    # Datos: [{'NomeMAY':'A CORUÑA', 'value':10}, {'NomeMAY':'SANTIAGO', 'value':15}...]
    data = list(Sample.objects.values('id_region__localizacion')\
            .filter(id_region__localizacion__gte=2)\
            .filter(fecha_muestra__range=[fecha_inicial, fecha_final])\
            .order_by().annotate(NomeMAY = F('id_region__localizacion') , value=Count('id_region__localizacion')))

    chart = {
        'chart':{
            'map':geojson_data,
        },
        'boost': {
            'seriesThreshold': 1,
            'useGPUTranslations': 'true'
        },
        'title': {
            'text': ''
        },    
        'colorAxis': {
            'tickPixelInterval': 100,
            'stops': [[0, '#ffe5e3'], [0.65, '#f04d55'], [1, '#f50a15']],
            # 'labels':{
            #     'format':'{value} x'
            # }
        },
        'tooltip': {
          'headerFormat': '',
          'pointFormat': '<b>{point.NomeMAY}</b><br>Total: {point.value}<br>Variante 1: 80%<br>Variante 2: 20%'
        },
        # 'mapNavigation': {
        #     'enabled': 'true',
        #     'buttonOptions': {
        #         'verticalAlign': 'bottom'
        #     }
        # },

        'series': [{
            'data': data,
            'keys': ['NomeMAY', 'value'],
            'joinBy': 'NomeMAY',
            'name': 'Muestras',
            'states': {
                'hover': {
                    'color': '#a4edba'
                }
            },
            'dataLabels': {
                'enabled': 'true',
                'format': '{point.properties.postal}'
            }           
        }],      
    }
    return JsonResponse(chart)

def hospital_graph(request, fecha_inicial, fecha_final):
    hospitales = SampleMetaData.objects.filter(id_uvigo__fecha_muestra__range=[fecha_inicial,fecha_final]).values('id_hospital')
    posibles_hospitales = hospitales.distinct()
    answer = []
    for i in posibles_hospitales:
        h = list(i.values())[0]
        c = hospitales.filter(id_hospital = h).count()
        answer.append({'name':h, 'y':int(c)})

    chart = {
        'plotOptions': {
            'series': {
                'animation': 'false'
            }
        },    
        'chart': {
            'type': 'pie',
        },
        'title': {'text': 'Origen de muestras'},
        'tooltip': {
            'pointFormat': '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        'accessibility': {
            'point': {
                'valueSuffix': '%'
            }
        },
        'plotOptions': {
            'pie': {
                'allowPointSelect': 'true',
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': 'true',
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }
        },  
        'series': [{
            'name': 'Cantidad',
            'data': answer # [{ name: 'CHHUVI', y: 1 }, { name: 'CHUAC', y: 1 }]
        }]
    }

    return JsonResponse(chart)

def variants_line_graph(request, fecha_inicial, fecha_final, variant):

    #######################
    ### Esto es para generar datos de prueba
    import random
    length = 30
    var = 10
    variantes = []
    for i in range(var):
        x = 'lugar' + str(i)
        variantes.append(x)
    dicc = {}
    for v in variantes:
        dicc[v] = []
        for l in range(length):
            x = round(random.normalvariate(0.5,0.2),2)
            dicc[v].append(x)

    from datetime import timedelta, date

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    start_dt = date(2021, 1, 1)
    end_dt = date(2021, 12, 30)
    dias = []
    for dt in daterange(start_dt, end_dt):
        dias.append(dt.strftime("%d/%m/%Y"))
    #############################

    # start = datetime.datetime.strptime("2021-01-01", "%Y-%m-%d")
    # end = datetime.datetime.strptime("2021-01-30", "%Y-%m-%d")
    # (end-start).days
    # date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

    chart = {
        'chart': {
            'scrollablePlotArea': {
                'minWidth': 700
            },
        },
        'title': {
            'text': f'Frecuencia de variante {variant} según lugar ({fecha_inicial}|{fecha_final})'
        },
        'subtitle': {
            'text': 'Source: Epicovigal'
        },
        'tooltip': {
            'shared': 'true',
            'crosshairs': 'true'
        },
        'xAxis': {
            'categories': dias
        },
        'legend': {
            'align': 'left',
            'verticalAlign': 'top',
            'borderWidth': 0
        },
        'series': [{
            'name': 'Spain',
            'data': dicc[variantes[0]]
        },{
            'name': 'France',
            'data': dicc[variantes[1]]
        },{
            'name': 'Portugal',
            'data': dicc[variantes[2]]
        },{
            'name': 'United States',
            'data': dicc[variantes[3]]
        },

        ]        
    }
    return JsonResponse(chart)

def variants_column_graph(request, fecha_inicial, fecha_final, variant):
    #######################
    ### Esto es para generar datos de prueba
    import random
    length = 10
    var = 10
    variantes = []
    for i in range(var):
        x = 'lugar' + str(i)
        variantes.append(x)
    dicc = {}
    for v in variantes:
        dicc[v] = []
        for l in range(length):
            x = round(random.normalvariate(0.5,0.2),2)
            dicc[v].append(x)

    from datetime import timedelta, date

    def daterange(date1, date2):
        for n in range(int ((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    start_dt = date(2021, 1, 1)
    end_dt = date(2021, 1, 30)
    dias = []
    for dt in daterange(start_dt, end_dt):
        dias.append(dt.strftime("%d/%m/%Y"))
    #############################
    chart = {
        'chart': {
            'type':'column'
        },
        'title': {
            'text': f'Proporción de variantes ({fecha_inicial}|{fecha_final})'
        },
        'subtitle': {
            'text': 'Source: Denmark'
        },
        'tooltip': {
            'shared': 'true',
            'crosshairs': 'true'
        },
        'xAxis': {
            'categories': dias
        },
        'legend': {
            'align': 'left',
            'verticalAlign': 'top',
            'borderWidth': 0
        },
        'tooltip': {
            'headerFormat': '<b>{point.x}</b><br/>',
            'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
        },
        'plotOptions': {
            'column': {
                'stacking': 'normal',
                'dataLabels': {
                    'enabled': 'true'
                }
            }
        },
        'series': [{
            'name': f'{variant}',
            'data': [483, 420, 601, 724, 977, 1412, 2206, 2122, 2335, 2512, 2282, 2099, 1448, 918, 577, 123]
        },{
            'name': 'N439K',
            'data': [217, 123, 157, 176, 244, 328, 530, 381, 435, 414, 377, 245, 114, 126, 75]
        },{
            'name': 'Resto',
            'data': [1435, 1229, 1623, 1734, 1979, 2690, 3951, 3576, 3908, 4135, 3956, 3680, 2657, 2225, 1821, 527]
        },

        ]        
    }
    return JsonResponse(chart)
