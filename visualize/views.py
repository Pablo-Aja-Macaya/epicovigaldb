from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import Counter
from django_tables2 import RequestConfig

from upload.models import Region, Sample
from upload.models import SampleMetaData 

from tests.models import LineagesTest, PicardTest, NextcladeTest, NGSstatsTest
from .models import CompletedTestsTable, SampleTable, RegionTable, SampleMetaDataTable, SingleCheckTest, VariantsTest
from .models import LineagesTable, PicardTable, NextcladeTable, NGSTable, VariantsTable, SingleCheckTable
from .models import SampleFilter, MetaDataFilter

def get_completed_tests():
    '''
    Devuelve para cada muestra si se ha hecho cada test
    '''
    lista = Sample.objects.values('id_uvigo','lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest')
    lista2 = []
    for i in lista:
        fields = ['lineagestest','nextcladetest','ngsstatstest','picardtest','singlechecktest','variantstest']
        for f in fields:
            try:
                int(i[f])
                i[f] = 1
            except:
                pass
        lista2.append(i)
    return lista2

@login_required(login_url="/accounts/login") 
def general(request):  
    
    hospital_list = []
    for i in Sample.objects.all():
        hospital_list.append(i.hospital_id())
    queryset = []
    hospital_count = Counter(i['id_uvigo'] for i in hospital_list)
    for k,v in hospital_count.items():
        queryset.append({'hospital':k, 'number':int(v)})

    table = CompletedTestsTable(get_completed_tests())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    

    return render(request, 'visualize/general.html', {'hospitals':queryset, 'table':table})
    

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



# @login_required(login_url="/accounts/login")
# def pruebatabla(request):
#     table = SampleTable(Sample.objects.all())
#     RequestConfig(request).configure(table)
#     table.paginate(page=request.GET.get("page", 1), per_page=50)
    
#     return render(request,'visualize/pruebatabla.html', {'table':table})



# @login_required(login_url="/accounts/login")
# def samples(request):
#     sample_fields = Sample._meta.get_fields()
#     samples = Sample.objects.order_by('id_uvigo').all()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(samples, 150)
    
#     try:
#         samples = paginator.page(page)
#     except PageNotAnInteger:
#         samples = paginator.page(1)
#     except EmptyPage:
#         samples = paginator.page(paginator.num_pages)    
    
#     return render(request, 'visualize/samples.html', {'samples':samples, 'sample_fields':sample_fields})