from django.shortcuts import render
from .models import Task
#from django.contrib.auth.decorators import login_required
from upload.models import Sample



#@login_required(login_url="/accounts/login")
def home(request):
    sample_count = Sample.objects.all().count()
    if request.user.is_authenticated:
        tasks = Task.objects
        url = 'tasks/home.html'
        return render(request, url, {'tasks':tasks, 'sample_count':sample_count})
    else:
        tasks = Task.objects.filter(show_to='all')
        url = 'tasks/visitor_home.html'
        return render(request, url, {'tasks':tasks, 'sample_count':sample_count})


##############
## Gráficas ##
from upload.models import SampleMetaData
from django.http import JsonResponse

def hospital_graph(request):
    hospitales = SampleMetaData.objects.values('id_hospital')
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
            'name': 'Porcentaje',
            'data': answer # [{ name: 'CHHUVI', y: 1 }, { name: 'CHUAC', y: 1 }]
        }]
    }

    return JsonResponse(chart)

def variants_line_graph(request, fecha, variant):

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

    chart = {
        'chart': {
            'scrollablePlotArea': {
                'minWidth': 700
            },
        },
        'title': {
            'text': f'Frecuencia de variante {variant} según lugar ({fecha})'
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

def variants_column_graph(request, fecha, variant):
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
            'text': f'Proporción de variantes ({fecha})'
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
