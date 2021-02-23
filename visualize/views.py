from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import Counter
from django_tables2 import RequestConfig

from upload.models import Region, Sample, SampleMetaData
from tests.models import LineagesTest, PicardTest, NextcladeTest, NGSstatsTest
from .models import SampleTable, RegionTable, SampleMetaDataTable, SingleCheckTest, VariantsTest
from .models import LineagesTable, PicardTable, NextcladeTable, NGSTable, VariantsTable, SingleCheckTable


@login_required(login_url="/accounts/login") 
def general(request):  
    
    hospital_list = []
    for i in Sample.objects.all():
        hospital_list.append(i.hospital_id())
    
    queryset = []
    hospital_count = Counter(i['id_uvigo'] for i in hospital_list)
    for k,v in hospital_count.items():
        queryset.append({'hospital':k, 'number':int(v)})
    
    return render(request, 'visualize/general.html', {'hospitals':queryset})
    

# Para metadatos
@login_required(login_url="/accounts/login")
def regions(request):
    table = RegionTable(Region.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/regions.html', {'table':table})   
    
@login_required(login_url="/accounts/login")
def samples(request):
    table = SampleTable(Sample.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)    
    return render(request, 'visualize/samples.html', {'table':table})

@login_required(login_url="/accounts/login")
def oursamplecharacteristics(request):
    table = SampleMetaDataTable(SampleMetaData.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)  
    
    return render(request, 'visualize/oursamplecharacteristics.html', {'table':table})

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