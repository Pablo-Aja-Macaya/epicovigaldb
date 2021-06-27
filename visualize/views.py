from os import X_OK
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import Counter
from django_tables2 import RequestConfig
from django.shortcuts import redirect
from django.contrib import messages
from django.forms.models import model_to_dict
from django.urls import reverse
from collections import OrderedDict
import base64
import datetime

from upload.models import Region, Sample
from upload.models import SampleMetaData 

from tests.models import VariantsTest, LineagesTest, PicardTest, NextcladeTest, NGSstatsTest, SingleCheckTest
# Tablas
from .models import SampleTable, RegionTable, SampleMetaDataTable, CompletedTestsTable
from .models import LineagesTable, PicardTable, NextcladeTable, NGSTable, VariantsTable, SingleCheckTable
# Filtros
from .models import SampleFilter, MetaDataFilter, RegionFilter
# Formularios
from .forms import GraphsForm, GraphsFormMultipleChoice
from .forms import SampleForm, SampleMetaDataForm, RegionForm
from .forms import SingleCheckForm, PicardForm, NextcladeForm, LineagesForm, NGSStatssForm

# In[0]
@login_required(login_url="/accounts/login") 
def get_graphs(request):
    url_origen = ''
    url_linajes_hospital = ''
    url_linajes = ''
    url_concellos = ''
    form = ''
    if request.method=='POST':
        form = GraphsForm(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            fecha_inicial = f['fecha_inicial'].strftime("%Y-%m-%d") 
            fecha_final = f['fecha_final'].strftime("%Y-%m-%d") 
            categoria = f['categoria']
            filtro = f['filtro']
            umbral = f['umbral']

            args = [fecha_inicial,fecha_final,categoria]
            args_sin_umbral = args.copy()
            args_con_umbral = args.copy()

            if umbral:
                args_con_umbral.append(umbral)
            if filtro:
                args_sin_umbral.append(filtro)
                args_con_umbral.append(filtro)

            url_origen = reverse('hospital_graph',args=args_sin_umbral)
            url_linajes_hospital = reverse('linajes_hospitales_graph',args=args_con_umbral)
            url_linajes = reverse('linajes_porcentaje_total',args=args_con_umbral)
            url_concellos = reverse('concellos_gal_graph',args=args_sin_umbral)            
    else:
        
        fecha_inicial = '2020-01-01'
        fecha_final = '2022-01-01'
        categoria = 'aleatoria'
        inicial = {'fecha_inicial':fecha_inicial, 'fecha_final':fecha_final, 'categoria':'aleatoria'}
        form = GraphsForm(initial=inicial)

        url_origen = reverse('hospital_graph',args=(fecha_inicial,fecha_final))
        url_linajes_hospital = reverse('linajes_hospitales_graph',args=(fecha_inicial,fecha_final))
        url_linajes = reverse('linajes_porcentaje_total',args=(fecha_inicial,fecha_final))
        url_concellos = reverse('concellos_gal_graph',args=(fecha_inicial,fecha_final))

    form2 = GraphsFormMultipleChoice()
    form2.fields['categoria'].choices = [(i,i) for i in Sample.objects.values_list('categoria_muestra',flat=True).distinct().order_by('categoria_muestra')]
    form2.fields['vigilancia'].choices = [(i,i) for i in Sample.objects.values_list('vigilancia',flat=True).distinct().order_by('vigilancia')]
    form2.fields['calidad_secuenciacion'].choices = [(i,i) for i in Sample.objects.values_list('samplemetadata__calidad_secuenciacion',flat=True).distinct().order_by('samplemetadata__calidad_secuenciacion')]

    context = {
        'url_form':reverse('get_graphs'),
        'url_origen' : url_origen,
        'url_linajes_hospital' : url_linajes_hospital,
        'url_linajes' : url_linajes,
        'url_concellos' : url_concellos,
        'form':form
        }
    return render(request, 'visualize/graphs.html', context)



def simple_url_encrypt(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return(base64_message)

def simple_url_decrypt(base64_message):
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = eval(message_bytes.decode('ascii'))
    return message


@login_required(login_url="/accounts/login") 
def get_graphs(request):
    encrypted_url_code = ''
    url_origen = ''
    url_linajes_hospital = ''
    url_linajes = ''
    url_concellos = ''
    if request.method=='POST':
        form = GraphsFormMultipleChoice(request.POST)
        if form.is_valid():
            f = form.cleaned_data
            f['fecha_inicial'] = f['fecha_inicial'].strftime("%Y-%m-%d") 
            f['fecha_final'] = f['fecha_final'].strftime("%Y-%m-%d") 
            
            # Encriptado
            string = str(dict(f))
            encrypted_url_code = simple_url_encrypt(string)

            # URLs de gráficas
            url_origen = reverse('hospital_graph',args=[encrypted_url_code])
            url_linajes = reverse('linajes_porcentaje_total',args=[encrypted_url_code])
            url_linajes_hospital = reverse('linajes_hospitales_graph',args=[encrypted_url_code])
            url_concellos = reverse('concellos_gal_graph',args=[encrypted_url_code])

            # Estado de filtro (colapsado/no colapsado)
            filter_collapse = ''
            

    else:
        fecha_inicial = '2020-01-01'
        fecha_final = '2022-01-01'
        categoria = 'aleatoria'
        inicial = {'fecha_inicial':fecha_inicial, 'fecha_final':fecha_final, 'categoria':'aleatoria'}
        
        form = GraphsFormMultipleChoice(initial=inicial)
        # Estado de filtro (colapsado/no colapsado)
        filter_collapse = 'show'

    context = {
        'url_form':reverse('get_graphs'),
        'form':form,
        'filter_collapse':filter_collapse,
        'encrypted_url_code':encrypted_url_code,
        'url_origen':url_origen,
        'url_linajes':url_linajes,
        'url_linajes_hospital':url_linajes_hospital,
        'url_concellos':url_concellos
        }
    return render(request, 'visualize/graphs_pruebas.html', context)

@login_required(login_url="/accounts/login") 
def drop_sample_cascade(request):
    if request.method=='POST':
        id_uvigo = request.POST.get('sample')
        sample = Sample.objects.get(id_uvigo=id_uvigo)
        sample.delete()
        
        messages.success(request, f'Todos los datos de {id_uvigo} han sido borrados.')
        return redirect(reverse('general'))


@login_required(login_url="/accounts/login") 
def edit_form(request, id_uvigo, tipo):
    lineage, clade, fecha_muestra, localizacion = Sample.objects.filter(id_uvigo=id_uvigo).values('lineagestest__lineage','nextcladetest__clade','fecha_muestra', 'id_region__localizacion')[0].values()
    
    def get_models(tipo):
        dicc = {
            # Metadatos
            'Sample':{
                'form_model':SampleForm,
                'model':Sample,
                'tittle':'Edición de metadatos comunes'
            },
            'SampleMetaData':{
                'form_model':SampleMetaDataForm,
                'model':SampleMetaData,
                'tittle':'Edición de metadatos extra'
            },
            # 'Region':{
            #     'form_model':RegionForm,
            #     'model':Region,
            #     'tittle':'Edición de regiones'
            # },
            ## Tests
            'SingleCheckTest':{
                'form_model':SingleCheckForm,
                'model':SingleCheckTest,
                'tittle':'Edición de test: SingleCheck'
            },
            'PicardTest':{
                'form_model':PicardForm,
                'model':PicardTest,
                'tittle':'Edición de test: Picard'
            },
            'NextcladeTest':{
                'form_model':NextcladeForm,
                'model':NextcladeTest,
                'tittle':'Edición de test: Nextclade'
            },
            'LineagesTest':{
                'form_model':LineagesForm,
                'model':LineagesTest,
                'tittle':'Edición de test: Pangolin'
            },
            'NGSstatsTest':{
                'form_model':NGSStatssForm,
                'model':NGSstatsTest,
                'tittle':'Edición de test: NGSStats'
            },
        }
        form_model = dicc[tipo]['form_model']
        model = dicc[tipo]['model']
        tittle = dicc[tipo]['tittle']
        return form_model, model, tittle

    form_model, model, tittle = get_models(tipo)

    if request.method=='POST':
        form = form_model(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            if tipo == 'Sample':
                datos.pop('id_uvigo',None)
                defaults = {'id_uvigo':id_uvigo, **datos}
                _, created = model.objects.update_or_create(
                        id_uvigo = id_uvigo,
                        defaults = defaults

                    )
            ## ARREGLAR EDICIÖN DE PANGOLIN
            # elif tipo == 'LineagesTest':
            #     pass
            else:
                datos['id_uvigo']=Sample.objects.get(id_uvigo=id_uvigo)
                _, created = model.objects.update_or_create(
                        id_uvigo = Sample.objects.get(id_uvigo=id_uvigo),
                        defaults = datos

                    )             
            messages.success(request, 'Cambios guardados')
            return redirect(reverse('specific_sample', args=(id_uvigo,)))
    else:
        try:
            obj = model.objects.get(id_uvigo=id_uvigo)
        except:
            obj = model(id_uvigo=Sample.objects.get(id_uvigo=id_uvigo))

        form = form_model(initial=model_to_dict(obj))

    context = {
        'id_uvigo':id_uvigo, 
        'lineage':lineage, 
        'clade':clade,
        'fecha_muestra':fecha_muestra,
        'localizacion':localizacion,
        'form':form,
        'url_muestra':reverse('specific_sample', args=(id_uvigo,)),
        'url_form':reverse('edit_form', args=(id_uvigo,tipo)),
        'tittle':tittle,
        # 'url_prueba':reverse('edit_form', args=(id_uvigo,tipo))
    }
    return render(request, 'visualize/edit_form.html', context)

def get_completed_tests(search=None):
    '''
    Devuelve para cada muestra si se ha hecho cada test
    '''
    # lista = Sample.objects.values('id_uvigo','lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest')
    if not search:
        lista = Sample.objects.values('id_uvigo').distinct().values('id_uvigo','lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest__id_uvigo').order_by('id_uvigo')
    else:
        lista = Sample.objects.values('id_uvigo').filter(id_uvigo__contains = search).distinct().values('id_uvigo','lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest__id_uvigo').order_by('id_uvigo')

    lista2 = []
    for i in lista:
        fields = ['lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest__id_uvigo']
        for f in fields:
            if i[f]!=None:
                # int(i[f])
                i[f] = 1

        lista2.append(i)
    return lista2



# In[1]
# Perfiles
@login_required(login_url="/accounts/login")
def specific_sample(request, id_uvigo): 
    # Datos generales
    lineage, clade, fecha_muestra, localizacion = Sample.objects.filter(id_uvigo=id_uvigo).values('lineagestest__lineage','nextcladetest__clade','fecha_muestra', 'id_region__localizacion')[0].values()
    prev_url = request.META.get('HTTP_REFERER')
    if not prev_url:
        prev_url = '/visualize/general'

    # Tablas
    sample_table = SampleTable(Sample.objects.filter(id_uvigo=id_uvigo))
    samplemetadata_table = SampleMetaDataTable(SampleMetaData.objects.filter(id_uvigo=id_uvigo))

    variants_table = VariantsTable(VariantsTest.objects.filter(id_uvigo=id_uvigo))
    singlecheck_table = SingleCheckTable(SingleCheckTest.objects.filter(id_uvigo=id_uvigo))
    picard_table = PicardTable(PicardTest.objects.filter(id_uvigo=id_uvigo))
    ngs_table = NGSTable(NGSstatsTest.objects.filter(id_uvigo=id_uvigo))
    nextclade_table = NextcladeTable(NextcladeTest.objects.filter(id_uvigo=id_uvigo))
    lineages_table = LineagesTable(LineagesTest.objects.filter(id_uvigo=id_uvigo))
    form_url = reverse('edit_form', args=(id_uvigo,'Sample'))
    context = {
        # Datos generales
        'id_uvigo':id_uvigo, 
        'lineage':lineage, 
        'clade':clade,
        'fecha_muestra':fecha_muestra,
        'localizacion':localizacion,
        'prev_url':prev_url,
        # Tablas
        'tablas':{
            'Metadatos comunes' : {form_url : sample_table},
            'Metadatos extra':{
                reverse('edit_form', args=(id_uvigo,'SampleMetaData')) : samplemetadata_table
            },
            'SingleCheck':{
                reverse('edit_form', args=(id_uvigo,'SingleCheckTest')) : singlecheck_table
            },
            'Picard':{
                reverse('edit_form', args=(id_uvigo,'PicardTest')) : picard_table}
            ,
            'NGSStats':{
                reverse('edit_form', args=(id_uvigo,'NGSstatsTest'))  : ngs_table
            },
            'Nextclade':{
                reverse('edit_form', args=(id_uvigo,'NextcladeTest')) : nextclade_table
                },
            'Pangolin':{
                reverse('edit_form', args=(id_uvigo,'LineagesTest')) : lineages_table
                },
            'iVar':{
                '#' : variants_table
            },
            },
        }
    return render(request, 'visualize/sample_profile.html', context)

@login_required(login_url="/accounts/login")
def specific_region(request, id_region):
    obj = Region.objects.get(id_region=id_region)
    
    if request.method=='POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            datos.pop('id_region',None)
            # datos.pop('localizacion',None)
            # datos.pop('cp',None)
            defaults = {
                'id_region':id_region,
                # 'localizacion':obj.localizacion,
                # 'cp':obj.cp,
                **datos
                }
            print(defaults)
            
            try:
                _, created = Region.objects.update_or_create(
                        id_region = id_region,
                        defaults = datos
                    ) 
                messages.success(request, 'Cambios guardados')
            except Exception as e:
                messages.warning(request, f'Error: {e}')
            return redirect(reverse('specific_region', args=(id_region,)))
    else:
        form = RegionForm(initial=model_to_dict(obj))

    prev_url = request.META.get('HTTP_REFERER')
    url_form = reverse('specific_region', args=(id_region,))
    context = {'obj':obj, 'prev_url':prev_url, 'url_form':url_form, 'form':form}
    return render(request, 'visualize/region_profile.html', context)

# General
@login_required(login_url="/accounts/login") 
def general(request):
    if request.method=='POST':
        search = request.POST.get('sample')
        table = CompletedTestsTable(get_completed_tests(search))
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get("page", 1), per_page=1000)
    else:
        table = CompletedTestsTable(get_completed_tests())
        RequestConfig(request).configure(table)
        table.paginate(page=request.GET.get("page", 1), per_page=50)    

    return render(request, 'visualize/general.html', {'table':table, 'filter':filter})




# In[2]
# Para tablas de metadatos
@login_required(login_url="/accounts/login")
def regions(request):
    data = Region.objects.all().order_by('localizacion')
    filter = RegionFilter(request.GET, queryset=data)
    data = filter.qs
    table = RegionTable(data)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)   
    context = {'table':table, 'filter':filter} 
    return render(request, 'visualize/regions.html', context)   
    
@login_required(login_url="/accounts/login")
def samples(request):
    data = Sample.objects.all().order_by('id_uvigo')
    filter = SampleFilter(request.GET, queryset=data)
    data = filter.qs

    table = SampleTable(data)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50) 
    context = {'table':table, 'filter':filter}

    return render(request, 'visualize/samples.html', context)

@login_required(login_url="/accounts/login")
def metadata(request):
    data = SampleMetaData.objects.all().order_by('id_uvigo')
    filter = MetaDataFilter(request.GET, queryset=data)
    data = filter.qs
    
    table = SampleMetaDataTable(data)
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50) 
    context = {'table':table, 'filter':filter}    
    return render(request, 'visualize/oursamplecharacteristics.html', context)

# Para tablas de resultados
@login_required(login_url="/accounts/login")
def lineages(request):
    table = LineagesTable(LineagesTest.objects.all().order_by('id_uvigo'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/lineages.html', {'table':table})

@login_required(login_url="/accounts/login")
def nextclade(request):
    table = NextcladeTable(NextcladeTest.objects.all().order_by('id_uvigo'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/nextclade.html', {'table':table})

@login_required(login_url="/accounts/login")
def ngsstats(request):
    table = NGSTable(NGSstatsTest.objects.all().order_by('id_uvigo'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/ngsstats.html', {'table':table})

@login_required(login_url="/accounts/login")
def picard(request):
    table = PicardTable(PicardTest.objects.all().order_by('id_uvigo'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/picard.html', {'table':table})

@login_required(login_url="/accounts/login")
def singlecheck(request):
    table = SingleCheckTable(SingleCheckTest.objects.all().order_by('id_uvigo'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/singlecheck.html', {'table':table})

@login_required(login_url="/accounts/login")
def variants(request):
    table = VariantsTable(VariantsTest.objects.all().order_by('id_uvigo'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/variants.html', {'table':table})



# In[3]
##############
## Gráficas ##
from upload.models import SampleMetaData
from django.http import JsonResponse
from django.db.models import F
from django.db.models import Count
from datetime import date, datetime
import geojson
from random import randint
from numpy import percentile


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

def get_graph_json_link(request, graph_base_url, fecha_inicial, fecha_final, categoria='aleatoria', filtro=None, umbral=None):
    # Devuelve un icono con el enlace de la gráfica si el usuario está loggeado
    if request.user.is_authenticated:
        args = [fecha_inicial,fecha_final,categoria]
        if umbral:
            args.append(umbral)
        if filtro:
            args.append(filtro)
        url = reverse(graph_base_url, args=args)
        json_link = f'<a href="{url}"><p style="color: rgb(61, 61, 255);">&#9741</p></a>'
        return json_link
    else:
        return ''

def linajes_porcentaje_total(request, encrypted_url_code):
    try:
        decrypted_dicc = simple_url_decrypt(encrypted_url_code)
        fecha_inicial = decrypted_dicc.get('fecha_inicial')
        fecha_final = decrypted_dicc.get('fecha_final')
        categoria = decrypted_dicc.get('categoria')
        vigilancia = decrypted_dicc.get('vigilancia')
        calidad_secuenciacion = decrypted_dicc.get('calidad_secuenciacion')
        filtro = decrypted_dicc.get('filtro')
        umbral = decrypted_dicc.get('umbral')
        
        if umbral is None:
            thresh = 4 # para eliminar variantes
        else:
            thresh = umbral

        linajes = Sample.objects.filter(vigilancia__in=vigilancia)\
                .filter(categoria_muestra__in=categoria)\
                .filter(samplemetadata__calidad_secuenciacion__in=calidad_secuenciacion)\
                .filter(id_uvigo__contains='EPI', fecha_muestra__range=[fecha_inicial, fecha_final])\
                .exclude(id_uvigo__contains='ICVS')

        # if categoria == 'vigilancia':
        #     linajes = Sample.objects.filter(vigilancia='si').filter(id_uvigo__contains='EPI', fecha_muestra__range=[fecha_inicial, fecha_final]).exclude(id_uvigo__contains='ICVS')
        # else:
        #     linajes = Sample.objects.filter(vigilancia='no').filter(id_uvigo__contains='EPI', categoria_muestra=categoria, fecha_muestra__range=[fecha_inicial, fecha_final]).exclude(id_uvigo__contains='ICVS')

        if filtro:
            linajes = linajes.filter(id_uvigo__contains=filtro)


        # if filtro:
        #     linajes = Sample.objects.filter(id_uvigo__contains=filtro).filter(id_uvigo__contains='EPI', categoria_muestra=categoria, fecha_muestra__range=[fecha_inicial, fecha_final]).exclude(id_uvigo__contains='ICVS')
        # else:
        #     linajes = Sample.objects.filter(id_uvigo__contains='EPI', categoria_muestra=categoria, fecha_muestra__range=[fecha_inicial, fecha_final]).exclude(id_uvigo__contains='ICVS')

        linajes_count = linajes\
            .values('lineagestest__lineage','samplemetadata__id_hospital')\
            .exclude(lineagestest__lineage__isnull=True)\
            .exclude(samplemetadata__id_hospital='ICVS')\
            .values('lineagestest__lineage')\
            .order_by('lineagestest__lineage')\
            .annotate(Count('lineagestest__lineage'))\
            .order_by('lineagestest__lineage__count').reverse()\
            .exclude(lineagestest__lineage='None')\
            .exclude(lineagestest__lineage__count__lte=thresh)


        lista_linajes = []
        lista_valores = []
        for i in linajes_count:
            lista_valores.append(i['lineagestest__lineage__count'])
            lista_linajes.append(i['lineagestest__lineage'])

        # print(lista_linajes)
        # print(lista_valores)
        # json_link = get_graph_json_link(request,'linajes_porcentaje_total', fecha_inicial, fecha_final, categoria, filtro, thresh)

        chart = {
            'chart': {
                'height': 400,
                'type': 'bar'
            },
            'title': {
                'text': f'Variantes en Galicia ({fecha_inicial} | {fecha_final}) ' # {json_link} ({fecha_inicial} | {fecha_final})
            },
            'subtitle': {
                'text': f'Categoría: {categoria}. Umbral: {thresh}'
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
    except Exception as e:
        print(e)
        chart = {}
    return JsonResponse(chart)

def linajes_hospitales_graph(request, encrypted_url_code):
    try:
        decrypted_dicc = simple_url_decrypt(encrypted_url_code)
        fecha_inicial = decrypted_dicc.get('fecha_inicial')
        fecha_final = decrypted_dicc.get('fecha_final')
        categoria = decrypted_dicc.get('categoria')
        vigilancia = decrypted_dicc.get('vigilancia')
        calidad_secuenciacion = decrypted_dicc.get('calidad_secuenciacion')
        filtro = decrypted_dicc.get('filtro')
        umbral = decrypted_dicc.get('umbral')

        percentil = 85
        
        linajes = Sample.objects.filter(vigilancia__in=vigilancia)\
                .filter(categoria_muestra__in=categoria)\
                .filter(samplemetadata__calidad_secuenciacion__in=calidad_secuenciacion)\
                .filter(id_uvigo__contains='EPI', fecha_muestra__range=[fecha_inicial, fecha_final])\
                .exclude(id_uvigo__contains='ICVS')

        if filtro:
            linajes = linajes.filter(id_uvigo__contains=filtro)

        linajes_count_with_hosp = linajes\
            .values('lineagestest__lineage','samplemetadata__id_hospital')\
            .exclude(lineagestest__lineage__isnull=True)\
            .order_by('lineagestest__lineage', 'samplemetadata__id_hospital')\
            .annotate(Count('lineagestest__lineage'))\
            .exclude(lineagestest__lineage='None')

        # Esto cuenta sólo cuánto hay de cada linaje
        linajes_count = linajes\
            .values('lineagestest__lineage')\
            .exclude(lineagestest__lineage__isnull=True)\
            .order_by('lineagestest__lineage')\
            .annotate(Count('lineagestest__lineage'))\
            .exclude(lineagestest__lineage='None')

        value_list = linajes_count.order_by('lineagestest__lineage__count').values_list('lineagestest__lineage__count',flat=True).reverse()
        
        if umbral is None:
            thresh = int(percentile(value_list,percentil))
        else:
            thresh = umbral

        linajes_otros = linajes_count.filter(lineagestest__lineage__count__lte=thresh)\
                                    .order_by('lineagestest__lineage__count')\
                                    .values_list('lineagestest__lineage', flat=True)
        linajes_principales = linajes_count.filter(lineagestest__lineage__count__gt=thresh)\
                                        .order_by('lineagestest__lineage__count')\
                                        .values_list('lineagestest__lineage', flat=True)


        # Se hace un set ordenado de los códigos de hospitales (CHUAC, CHUS...)
        lista_hospitales = [i['samplemetadata__id_hospital'] for i in linajes_count_with_hosp]
        lista_hospitales = sorted(set(lista_hospitales))

        drilldown_dicc = {}
        # drilldown_dicc = {
        #     'HOSP-Otros':{
        #         'id':'HOSP-Otros',
        #         'name':'Otros',
        #         'data':{
        #             'LINAJE':{'name':'LINAJE','y':1}
        #         }
        #     }
        # }
        series_dicc = {}
        series_dicc['Otros'] = {'name':'Otros','data':{}}
        for i in linajes_count_with_hosp:
            hosp = i['samplemetadata__id_hospital']
            linaje = i['lineagestest__lineage']
            count = i['lineagestest__lineage__count']
            # pos_hosp = lista_hospitales.index(hosp) # posición del hospital en el set de hospitales
            
            # Linaje superó el umbral de conteo impuesto
            if linaje in linajes_principales:
                drilldown_id = hosp+'-'+linaje
                # Si todavía no se ha visto la variante
                if linaje not in series_dicc.keys():
                    series_dicc[linaje] = {
                        'name':linaje,
                        'data':{
                            hosp:{'name':hosp, 'y':count, 'drilldown':drilldown_id}
                        }
                    }
                # Si se ha visto la variante
                else: 
                    if hosp in series_dicc[linaje]['data'].keys():
                        series_dicc[linaje]['data'][hosp]['y'] +=count
                    else:
                        series_dicc[linaje]['data'][hosp]={'name':hosp, 'y':count, 'drilldown':drilldown_id}
            
            # Linaje no superó el umbral de conteo impuesto
            elif linaje in linajes_otros:
                drilldown_id = hosp+'-'+'Otros'
                name = hosp+'-'+linaje
                # Si todavía no se ha visto el hospital
                if hosp not in series_dicc['Otros']['data'].keys():
                    series_dicc['Otros']['data'][hosp] = {
                        'name':hosp, 
                        'y':count, 
                        'drilldown':drilldown_id
                    }
                    drilldown_dicc[drilldown_id] = {
                        'id':drilldown_id,
                        'name':'Otros',
                        'stacking':'normal',
                        'data':{linaje:{'name':name, 'y':count}},
                        'tooltip':{
                            'headerFormat': '<span style="font-size:10px"><strong>{series.name}</strong></span><table>',
                            'pointFormat': '<tr><td style="color:{series.color};padding:0;"><strong>{point.name}:</strong> </td>' +
                                '<td style="padding:0"> <strong>&nbsp;{point.y}</strong> </td></tr>',
                            'footerFormat': '</table>',
                            'shared': True,
                            'backgroundColor':'#FFFFFF',
                            'useHTML': True
                        },       
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y}'
                        },  
                    }
                # Si se ha visto el hospital
                else:
                    series_dicc['Otros']['data'][hosp]['y'] +=count
                    if linaje not in drilldown_dicc[drilldown_id]['data'].keys():
                        drilldown_dicc[drilldown_id]['data'][linaje] = {'name':name, 'y':count}
                    else:
                        drilldown_dicc[drilldown_id]['data'][linaje]['y'] += count

        # Ordenar series_dicc para que los linajes con más cantidad aparezcan a la izquierda de la gráfica
        orden = ['Otros']
        orden += linajes_principales
        series_dicc = OrderedDict(sorted(series_dicc.items(),key=lambda pair: orden.index(pair[0]),reverse=True))
        # Transformar diccionarios en listas
        for i in series_dicc.keys():
            series_dicc[i]['data'] = list(series_dicc[i]['data'].values())
        for i in drilldown_dicc.keys():
            drilldown_dicc[i]['data'] = list(drilldown_dicc[i]['data'].values())
            drilldown_dicc[i]['data'] = sorted(drilldown_dicc[i]['data'], key=lambda k: k['y'], reverse=True)

        for lin in series_dicc.keys():
            if lin != 'Otros':
                for d in series_dicc[lin]['data']:
                    drilldown_id = d['drilldown']
                    drilldown_dicc[drilldown_id] = {
                        'id':drilldown_id,
                        'name':lin,
                        'data':[{'name':drilldown_id, 'y':d['y']}],
                        'stacking':'normal',
                        'tooltip':{
                            'headerFormat': '<span style="font-size:10px"><strong>{series.name}</strong></span><table>',
                            'pointFormat': '<tr><td style="color:{series.color};padding:0;"><strong>{point.name}:</strong> </td>' +
                                '<td style="padding:0"> <strong>&nbsp;{point.y}</strong> </td></tr>',
                            'footerFormat': '</table>',
                            'shared': True,
                            'backgroundColor':'#FFFFFF',
                            'useHTML': True
                        },       
                        'dataLabels': {
                            'enabled': True,
                            'format': '{point.y}'
                        }, 
                    }

        drilldown_dicc = OrderedDict(sorted(drilldown_dicc.items()))
        # json_link = get_graph_json_link(request,'linajes_hospitales_graph', fecha_inicial, fecha_final, categoria, filtro, thresh)
        chart_height = 700
        chart = {
            'chart': {
                'height': chart_height,
                'type': 'bar'
            },
            'title': {
                'text': f'Variantes por hospital ({fecha_inicial} | {fecha_final}) ' #{json_link} ({fecha_inicial} | {fecha_final})
            },
            'subtitle': {
                'text': f'Pulsa sobre el nombre de un hospital para ver todos los linajes. Categoría: {categoria}. Umbral: {thresh}'
            },
            'xAxis': {
                'type':'category'
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
            'lang': {
                'drillUpText': '<strong><< Atrás</strong>'
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
                    'pointWidth': 25,
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
            'series': list(series_dicc.values()),
            'drilldown':{
                'activeAxisLabelStyle': {
                    'textDecoration': None,
                },
                'activeDataLabelStyle': {
                    'textDecoration': 'none',
                    'color':'white'
                },
                'drillUpButton':{
                    'position':{
                        # 'x':0,
                        'y':chart_height-200
                    }
                },
                'series':list(drilldown_dicc.values())
            }
            # }
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
    except Exception as e:
        print(e)
        chart = {}
    return JsonResponse(chart)

def concellos_gal_graph(request, encrypted_url_code):
    map_file = './mapas_galicia/GaliciaConcellos_Simple.geojson'
    map_file = './mapas_galicia/GaliciaConcellos_reduccion.geojson'
    
    
    # map_file = '/home/pabs/GaliciaComarcas.geojson'
    with open(map_file) as map:
        geojson_data = geojson.load(map) # mapa
    
    try:
        
        decrypted_dicc = simple_url_decrypt(encrypted_url_code)
        fecha_inicial = decrypted_dicc.get('fecha_inicial')
        fecha_final = decrypted_dicc.get('fecha_final')
        categoria = decrypted_dicc.get('categoria')
        vigilancia = decrypted_dicc.get('vigilancia')
        calidad_secuenciacion = decrypted_dicc.get('calidad_secuenciacion')
        filtro = decrypted_dicc.get('filtro')
        umbral = decrypted_dicc.get('umbral')

        data = Sample.objects.filter(vigilancia__in=vigilancia)\
                .filter(categoria_muestra__in=categoria)\
                .filter(samplemetadata__calidad_secuenciacion__in=calidad_secuenciacion)\
                .filter(id_uvigo__contains='EPI', fecha_muestra__range=[fecha_inicial, fecha_final])\
                .exclude(id_uvigo__contains='ICVS')

        if filtro:
            data = data.filter(id_uvigo__contains=filtro)

        # Datos: [{'NomeMAY':'A CORUÑA', 'value':10}, {'NomeMAY':'SANTIAGO', 'value':15}...]
        data = list(data.filter(id_uvigo__contains='EPI').exclude(id_uvigo__contains='ICVS')\
                .values('id_region__localizacion')\
                .filter(id_region__localizacion__gte=2)\
                .filter(fecha_muestra__range=[fecha_inicial, fecha_final])\
                .order_by().annotate(NomeMAY = F('id_region__localizacion') , value=Count('id_region__localizacion')))

        

        # json_link = get_graph_json_link(request,'concellos_gal_graph', fecha_inicial, fecha_final, categoria, filtro)
        chart = {
            'chart':{
                'map':geojson_data,
            },
            'boost': {
                'seriesThreshold': 1,
                'useGPUTranslations': True
            },
            'title': {
                'text': f'Geolocalización ({fecha_inicial} | {fecha_final}) ' #{json_link} ({fecha_inicial} | {fecha_final})
            },
            'subtitle': {
                'text': f'Muestras en cada concello. Categoría: {categoria}'
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
    except:
        chart = {}
    return JsonResponse(chart)

def hospital_graph(request, encrypted_url_code):
    try:
        decrypted_dicc = simple_url_decrypt(encrypted_url_code)
        fecha_inicial = decrypted_dicc.get('fecha_inicial')
        fecha_final = decrypted_dicc.get('fecha_final')
        categoria = decrypted_dicc.get('categoria')
        vigilancia = decrypted_dicc.get('vigilancia')
        filtro = decrypted_dicc.get('filtro')
        calidad_secuenciacion = decrypted_dicc.get('calidad_secuenciacion')
        
        hospitales = SampleMetaData.objects.filter(id_uvigo_id__categoria_muestra__in=categoria)\
                    .filter(calidad_secuenciacion__in=calidad_secuenciacion)\
                    .filter(id_uvigo_id__vigilancia__in=vigilancia)\
                    .filter(id_uvigo_id__id_uvigo__contains='EPI', id_uvigo__fecha_muestra__range=[fecha_inicial, fecha_final])\
                    .exclude(id_uvigo_id__id_uvigo__contains='ICVS')

        if filtro:
            hospitales = hospitales.filter(id_uvigo_id__id_uvigo__contains=filtro).values('id_hospital')
        else:
            hospitales = hospitales.values('id_hospital')

        
        posibles_hospitales = hospitales.distinct()
        answer = []
        for i in posibles_hospitales:
            h = list(i.values())[0]
            c = hospitales.filter(id_hospital = h).count()
            answer.append({'name':h, 'y':int(c)})

        # json_link = get_graph_json_link(request,'hospital_graph', fecha_inicial, fecha_final, categoria, filtro)
        chart = {
            'chart': {
                'type': 'pie',
            },
            'title': {'text': f'Origen de muestras ({fecha_inicial} | {fecha_final}) '}, #{json_link}
            'subtitle': {
                'text': f'Origen de muestras recibidas (Incluyendo secuenciadas y no secuenciadas). Categoría: {categoria}.'
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
    except Exception as e:
        print(e)
        chart = {}
    return JsonResponse(chart)




# No usadas
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


