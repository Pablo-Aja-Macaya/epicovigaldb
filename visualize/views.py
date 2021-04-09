from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import Counter
from django_tables2 import RequestConfig

from upload.models import Region, Sample
from upload.models import SampleMetaData 

from tests.models import LineagesTest, PicardTest, NextcladeTest, NGSstatsTest
from .models import *
# from .models import CompletedTestsTable, SampleTable, RegionTable, SampleMetaDataTable, SingleCheckTest, VariantsTest
# from .models import LineagesTable, PicardTable, NextcladeTable, NGSTable, VariantsTable, SingleCheckTable
# from .models import SampleFilter, MetaDataFilter,CompletedTestsFilter

def get_completed_tests():
    '''
    Devuelve para cada muestra si se ha hecho cada test
    '''
    # lista = Sample.objects.values('id_uvigo','lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest')
    lista = Sample.objects.values('id_uvigo').distinct().values('id_uvigo','lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest__id_uvigo')
    lista2 = []
    for i in lista:
        fields = ['lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest__id_uvigo']
        for f in fields:
            if i[f]!=None:
                # int(i[f])
                i[f] = 1

        lista2.append(i)
    return lista2

@login_required(login_url="/accounts/login") 
def general(request):  
    table = CompletedTestsTable(get_completed_tests())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    

    return render(request, 'visualize/general.html', {'table':table, 'filter':filter})
    

# Para metadatos
@login_required(login_url="/accounts/login")
def regions(request):
    table = RegionTable(Region.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/regions.html', {'table':table})   
    
@login_required(login_url="/accounts/login")
def samples(request):
    data = Sample.objects.all()
    filter = SampleFilter(request.GET, queryset=data)
    data = filter.qs

    table = SampleTable(data)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50) 
    context = {'table':table, 'filter':filter}

    return render(request, 'visualize/samples.html', context)

@login_required(login_url="/accounts/login")
def metadata(request):
    data = SampleMetaData.objects.all()
    filter = MetaDataFilter(request.GET, queryset=data)
    data = filter.qs
    
    table = SampleMetaDataTable(data)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50) 
    context = {'table':table, 'filter':filter}    
    return render(request, 'visualize/oursamplecharacteristics.html', context)

# Para resultados
@login_required(login_url="/accounts/login")
def lineages(request):
    table = LineagesTable(LineagesTest.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/lineages.html', {'table':table})

@login_required(login_url="/accounts/login")
def nextclade(request):
    table = NextcladeTable(NextcladeTest.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/nextclade.html', {'table':table})

@login_required(login_url="/accounts/login")
def ngsstats(request):
    table = NGSTable(NGSstatsTest.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/ngsstats.html', {'table':table})

@login_required(login_url="/accounts/login")
def picard(request):
    table = PicardTable(PicardTest.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/picard.html', {'table':table})

@login_required(login_url="/accounts/login")
def singlecheck(request):
    table = SingleCheckTable(SingleCheckTest.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/singlecheck.html', {'table':table})

@login_required(login_url="/accounts/login")
def variants(request):
    table = VariantsTable(VariantsTest.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/variants.html', {'table':table})

@login_required(login_url="/accounts/login")
def specific_sample(request, id_uvigo): 
    # Datos generales
    lineage, clade, fecha_muestra, localizacion = Sample.objects.filter(id_uvigo=id_uvigo).values('lineagestest__lineage','nextcladetest__clade','fecha_muestra', 'id_region__localizacion')[0].values()
    
    # Tablas
    sample_table = SampleTable(Sample.objects.filter(id_uvigo=id_uvigo))
    samplemetadata_table = SampleMetaDataTable(SampleMetaData.objects.filter(id_uvigo=id_uvigo))

    variants_table = VariantsTable(VariantsTest.objects.filter(id_uvigo=id_uvigo))
    singlecheck_table = SingleCheckTable(SingleCheckTest.objects.filter(id_uvigo=id_uvigo))
    picard_table = PicardTable(PicardTest.objects.filter(id_uvigo=id_uvigo))
    ngs_table = NGSTable(NGSstatsTest.objects.filter(id_uvigo=id_uvigo))
    nextclade_table = NextcladeTable(NextcladeTest.objects.filter(id_uvigo=id_uvigo))
    lineages_table = LineagesTable(LineagesTest.objects.filter(id_uvigo=id_uvigo))
    
    context = {
        # Datos generales
        'id_uvigo':id_uvigo, 
        'lineage':lineage, 
        'clade':clade,
        'fecha_muestra':fecha_muestra,
        'localizacion':localizacion,
        # Tablas
        'tablas':{
            'Metadatos comunes':sample_table,
            'Metadatos extra':samplemetadata_table,
            'SingleCheck':singlecheck_table,
            'Picard':picard_table,
            'NGSStats':ngs_table,
            'Nextclade':nextclade_table,
            'Pangolin':lineages_table,
            'iVar':variants_table,
            },
        }
    return render(request, 'visualize/sample_profile.html', context)


##############
## Gráficas ##
from upload.models import SampleMetaData
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Count
from datetime import date, datetime
import geojson
from random import randint

credits = {
    'enabled': True,'text':
    'epicovigaldb.com',
    'href':'https://epicovigaldb.com',
    'style':{'fontSize':15}
    }

COLOR_LIST = [
    '#f0e68c','#fa8072','#ffff54',
    '#6495ed','#dda0dd','#90ee90',
    '#ff1493','#7b68ee','#afeeee',
    '#483d8b','#cd853f','#9acd32',
    '#20b2aa','#00008b','#32cd32',
    '#8fbc8f','#8b008b','#b03060',
    '#ff4500','#ffa500','#7fff00',
    '#9400d3','#dc143c','#00ffff',
    '#00bfff','#0000ff','#ff00ff',
    '#a9a9a9','#2f4f4f','#556b2f',
    '#228b22','#7f0000','#808000',
    '#ffe4c4','#ffb6c1',
]

def linajes_porcentaje_total(request, fecha_inicial, fecha_final):
    thresh = 2 # para eliminar variantes 
    linajes_count = Sample.objects.filter(categoria_muestra='aleatoria',fecha_muestra__range=[fecha_inicial, fecha_final])\
        .values('lineagestest__lineage','samplemetadata__id_hospital')\
        .exclude(lineagestest__lineage__isnull=True)\
        .exclude(samplemetadata__id_hospital='ICVS')\
        .values('lineagestest__lineage')\
        .order_by('lineagestest__lineage')\
        .annotate(Count('lineagestest__lineage'))\
        .exclude(lineagestest__lineage='None')\
        .exclude(lineagestest__lineage__count__lt = thresh)

    lista_linajes = []
    lista_valores = []
    for i in linajes_count:
        lista_valores.append(i['lineagestest__lineage__count'])
        lista_linajes.append(i['lineagestest__lineage'])

    # print(lista_linajes)
    # print(lista_valores)
    chart = {
        'chart': {
            'height': 400,
            'type': 'bar'
        },
        'title': {
            'text': f'Variantes en Galicia ({fecha_inicial} | {fecha_final})' # ({fecha_inicial} | {fecha_final})
        },
        'subtitle': {
            'text': f'Variantes que aparecen, al menos, {thresh} veces (Muestras aleatorias, sin incluir al ICVS).'
        },
        'xAxis': {
            'categories': lista_linajes,
            'title': {
                'text': ''
            },
            'labels': {
                'style': {
                    'fontWeight': 'bold',
                    # 'color': 'red'
                }
            }
        },
        'tooltip': {
            # 'valueSuffix': ' %'
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Cantidad',
                'align': 'middle'
            },
            'labels': {
                'overflow': 'justify'
            }
        },
        'plotOptions': {
            'bar': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.y}'
                },
                
            },
            'series': {
                'pointWidth': 8,
                'animation': False
            }
        },
        'credits':credits,
        'series': [{
            'name':'Cantidad',
            'showInLegend': False, 
            'data': lista_valores
        }
        ]
    }
    return JsonResponse(chart)

def linajes_hospitales_graph(request, fecha_inicial, fecha_final):
    # Query que cuenta las veces que aparece una variante en cada hospital
    # Estructura:
    # <QuerySet [{'lineagestest__lineage': 'B.1.177', 'samplemetadata__id_hospital': 'CHUF', 'lineagestest__lineage__count': 1}, 
    # {'lineagestest__lineage': 'B.1.177', 'samplemetadata__id_hospital': 'HULA', 'lineagestest__lineage__count': 1}]>
    linajes_count = Sample.objects.filter(categoria_muestra='aleatoria',fecha_muestra__range=[fecha_inicial, fecha_final])\
        .values('lineagestest__lineage','samplemetadata__id_hospital')\
        .exclude(lineagestest__lineage__isnull=True)\
        .order_by('lineagestest__lineage', 'samplemetadata__id_hospital')\
        .annotate(Count('lineagestest__lineage'))\
        .exclude(lineagestest__lineage='None')
    # .exclude(lineagestest__lineage__count__lt = thresh)

    # Se hace un set ordenado de los códigos de hospitales (CHUAC, CHUS...)
    lista_hospitales = [i['samplemetadata__id_hospital'] for i in linajes_count]
    lista_hospitales = sorted(set(lista_hospitales))

    series_dicc = {}
    for i in linajes_count:
        # print(i)
        hosp = i['samplemetadata__id_hospital']
        linaje = i['lineagestest__lineage']
        count = i['lineagestest__lineage__count']
        pos_hosp = lista_hospitales.index(hosp) # posición del hospital en el set de hospitales
        
        # Si todavía no se ha visto la variante
        if linaje not in series_dicc.keys():
            # Se inicializa una lista de Nones 
            tmp_list = [None for i in range(len(lista_hospitales))]
            # En la posición del hospital se pone el valor para ese hospital
            tmp_list[pos_hosp] = count
            series_dicc[linaje] = {
                'name':linaje,
                'data':tmp_list
            }
        # Si se ha visto la variante
        else:
            # Si ya hay una cuenta para cierto hospital (en esta posición None a pasado a ser un número)
            if series_dicc[linaje]['data'][pos_hosp]:
                series_dicc[linaje]['data'][pos_hosp] += count
            # Si este hospital todavía no se ha visto
            else:
                series_dicc[linaje]['data'][pos_hosp] = count

    
    # Quitar variantes que no aparecen más de N veces en ningún hospital 
    thresh = 3
    series_dicc_mod = {}
    for i in series_dicc.keys():
        keep = False
        for n in series_dicc[i]['data']:
            if n and n>thresh:
                keep=True
        if keep == True:
            series_dicc_mod[i] = series_dicc[i]
            series_dicc_mod[i]['drilldown'] = i

    # print(series_dicc_mod)
    # Estructura de series_dicc
    # dicc = {
    #     'linaje1':{
    #         'name':'linaje1',
    #         'data':[1,2,3]
    #     },
    #     'linaje2':{
    #         'name':'linaje2',
    #         'data':[1,2,3]
    #     }
    # }

    chart = {
        'chart': {
            'height': 500,
            'type': 'bar'
        },
        'title': {
            'text': f'Variantes por hospital ({fecha_inicial} | {fecha_final})' # ({fecha_inicial} | {fecha_final})
        },
        'subtitle': {
            'text': f'Variantes que aparecen, al menos, {thresh} veces en algún hospital (Muestras aleatorias).'
        },
        'xAxis': {
            'categories': lista_hospitales,
            'title': {
                'text': None
            },
            'labels': {
                'style': {
                    'fontWeight': 'bold',
                    # 'color': 'red'
                }
            }
        },
        'yAxis': {
            'min': 0,
            'title': {
                'text': 'Porcentaje',
                'align': 'middle'
            },
            'labels': {
                'overflow': 'justify'
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:10px"><strong>{point.key}</strong></span><table>',
            'pointFormat': '<tr><td style="color:{series.color};padding:0;"><strong>{series.name}:</strong> </td>' +
                '<td style="padding:0"> <strong>&nbsp;{point.y}</strong> ({point.percentage:.0f}%) </td></tr>',
            'footerFormat': '</table>',
            'shared': True,
            'backgroundColor':'#FFFFFF',
            'useHTML': True
        },
        'plotOptions': {
            'bar': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.percentage:.0f}%'
                }
            },
            'series': {
                # 'groupPadding': 10,
                'stacking': 'percent',
                'pointPadding': 1,
                'pointWidth': 20,
                'animation': False
            }
        },
        'legend': {
            'layout': 'horizontal',
            'align': 'center',
            'verticalAlign': 'bottom',
            'x': 10,
            # 'y': 60,
            # 'floating': True,
            # 'borderWidth': 0.5,
            # 'shadow': True
        },
        # 'colors': COLOR_LIST,
        'credits': credits,
        'series': list(series_dicc_mod.values()),
        'drilldown':{
            'series':[{
                    # 'name':'B.1',
                    'id':'B.1',
                    'data':[
                        ["v58.0",1.02],
                        ["v57.0",7.36],                        
                    ]
                }
            ]

        }
        # {
        #     'name': 'Error B.1',
        #     'type': 'errorbar',
        #     'yAxis': 0,
        #     'data': [[None,None], [None,None], [None,None], [None,None], [None,None], [0.5,1.5], [None,None]],
        #     # 'tooltip': {
        #     #     'pointFormat': 'Rango error: {point.low}-{point.high}'
        #     # },
        #     'stemWidth': 1,
        #     'whiskerLength': 5
        # },
        
    }
    return JsonResponse(chart)

def concellos_gal_graph(request, fecha_inicial, fecha_final):
    map_file = './mapas_galicia/GaliciaConcellos_Simple.geojson'
    map_file = './mapas_galicia/GaliciaConcellos_reduccion.geojson'
    
    # map_file = '/home/pabs/GaliciaComarcas.geojson'
    with open(map_file) as map:
        geojson_data = geojson.load(map) # mapa
    
    # Datos: [{'NomeMAY':'A CORUÑA', 'value':10}, {'NomeMAY':'SANTIAGO', 'value':15}...]
    data = list(Sample.objects.filter(categoria_muestra='aleatoria')\
            .values('id_region__localizacion')\
            .filter(id_region__localizacion__gte=2)\
            .filter(fecha_muestra__range=[fecha_inicial, fecha_final])\
            .order_by().annotate(NomeMAY = F('id_region__localizacion') , value=Count('id_region__localizacion')))
            
    chart = {
        'chart':{
            'map':geojson_data,
        },
        'boost': {
            'seriesThreshold': 1,
            'useGPUTranslations': True
        },
        'title': {
            'text': f'Geolocalización ({fecha_inicial} | {fecha_final})' # ({fecha_inicial} | {fecha_final})
        },
        'subtitle': {
            'text': f'Muestras aleatorias en cada concello.'
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
          'pointFormat': '<b>{point.NomeMAY}</b><br>Total: {point.value}'
        },
        # 'mapNavigation': {
        #     'enabled': 'true',
        #     'buttonOptions': {
        #         'verticalAlign': 'bottom'
        #     }
        # },
        'plotOptions': {
            'series': {
                'animation': False
            }
        },
        'credits': credits,
        'series': [{
            'boostThreshold': 1,
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
                'enabled': True,
                'format': '{point.properties.postal}'
            }           
        }],      
    }
    return JsonResponse(chart)

def hospital_graph(request, fecha_inicial, fecha_final):
    hospitales = SampleMetaData.objects.filter(id_uvigo_id__categoria_muestra='aleatoria',id_uvigo__fecha_muestra__range=[fecha_inicial,fecha_final]).values('id_hospital')
    posibles_hospitales = hospitales.distinct()
    answer = []
    for i in posibles_hospitales:
        h = list(i.values())[0]
        c = hospitales.filter(id_hospital = h).count()
        answer.append({'name':h, 'y':int(c)})

    chart = {
        'chart': {
            'type': 'pie',
        },
        'title': {'text': f'Origen de muestras ({fecha_inicial} | {fecha_final})'},
        'subtitle': {
            'text': f'Origen de muestras aleatorias recibidas (Incluyendo secuenciadas y no secuenciadas)'
        },
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
                'allowPointSelect': True,
                'cursor': 'pointer',
                'dataLabels': {
                    'enabled': True,
                    'format': '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            },
            'series': {
                'animation': False
            }
        },
        'credits': credits,
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
            'shared': True,
            'crosshairs': True
        },
        'xAxis': {
            'categories': dias
        },
        'legend': {
            'align': 'left',
            'verticalAlign': 'top',
            'borderWidth': 0
        },
        'plotOptions': {
            'series': {
                'animation': False
            }
        },
        'credits': credits,
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
            'shared': True,
            'crosshairs': True
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
                    'enabled': True
                }
            },
            'series': {
                'animation': False
            }
        },
        'credits':credits,
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




dicc = {
    'B.1':{
        'name':'B.1',
        'data':{
            'CHUVI':{'name': 'CHUVI', 'y': 100, 'drilldown': 'chuvi-B.1'},
            'CHUAC':{'name': 'CHUAC', 'y': 60, 'drilldown': 'chuac-B.1'},
        }
    }
}

# from django.db.models import Count

# linajes_count = Sample.objects.filter(categoria_muestra='aleatoria',fecha_muestra__range=['2020-01-01', '2030-01-01'])\
#     .values('lineagestest__lineage','samplemetadata__id_hospital')\
#     .exclude(lineagestest__lineage__isnull=True)\
#     .order_by('lineagestest__lineage', 'samplemetadata__id_hospital')\
#     .annotate(Count('lineagestest__lineage'))\
#     .exclude(lineagestest__lineage='None')
# # .exclude(lineagestest__lineage__count__lt = thresh)

# # Se hace un set ordenado de los códigos de hospitales (CHUAC, CHUS...)
# lista_hospitales = [i['samplemetadata__id_hospital'] for i in linajes_count]
# lista_hospitales = sorted(set(lista_hospitales))

# series_dicc = {}
# for i in linajes_count:
#     hosp = i['samplemetadata__id_hospital']
#     linaje = i['lineagestest__lineage']
#     count = i['lineagestest__lineage__count']
#     pos_hosp = lista_hospitales.index(hosp) # posición del hospital en el set de hospitales
    
#     # Si todavía no se ha visto la variante
#     if linaje not in series_dicc.keys():
#         series_dicc[linaje] = {
#             'name':linaje,
#             'data':{
#                 hosp:{'name':hosp, 'y':count, 'drilldown':hosp+'-'+linaje}
#             }
#         }
#     # Si se ha visto la variante
#     else: 
#         if hosp in series_dicc[linaje]['data'].keys():
#             series_dicc[linaje]['data'][hosp]['y'] +=count
#         else:
#             series_dicc[linaje]['data'][hosp]={'name':hosp, 'y':count, 'drilldown':hosp+'-'+linaje}

# for i in series_dicc.keys():
#     series_dicc[i]['data'] = list(series_dicc[i]['data'].values())
#     if len(series_dicc[i]['data'])<2:
#         keep = False
#         for n,d in enumerate(series_dicc[i]['data']):
#             if series_dicc[i]['data'][n]['y'] <= 3:
#                 drill_id = series_dicc[i]['data'][n]['drilldown'] 
#                 series_dicc[i]['data'][n]['drilldown'] = drill_id.split('-')[0]+'-otros'
#                 print(i, series_dicc[i]['data'][n])