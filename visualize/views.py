from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Region, Sample, SampleMetaData
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from collections import Counter
from .models import SampleTable
from django_tables2 import RequestConfig

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
    

@login_required(login_url="/accounts/login")
def regions(request):
    region_fields = Region._meta.get_fields()
    regions = Region.objects.order_by('localizacion','cp').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(regions, 150)    
    
    try:
        regions = paginator.page(page)
    except PageNotAnInteger:
        regions = paginator.page(1)
    except EmptyPage:
        regions = paginator.page(paginator.num_pages)    
    
    return render(request, 'visualize/regions.html', {'regions':regions, 'region_fields':region_fields})

@login_required(login_url="/accounts/login")
def samples(request):
    sample_fields = Sample._meta.get_fields()
    samples = Sample.objects.order_by('id_uvigo').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(samples, 150)
    
    try:
        samples = paginator.page(page)
    except PageNotAnInteger:
        samples = paginator.page(1)
    except EmptyPage:
        samples = paginator.page(paginator.num_pages)    
    
    return render(request, 'visualize/samples.html', {'samples':samples, 'sample_fields':sample_fields})

@login_required(login_url="/accounts/login")
def oursamplecharacteristics(request):
    oursamplecharacteristics_fields = SampleMetaData._meta.get_fields()
    oursamplecharacteristics = SampleMetaData.objects.order_by('id_uvigo').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(oursamplecharacteristics, 150)
    
    try:
        oursamplecharacteristics = paginator.page(page)
    except PageNotAnInteger:
        oursamplecharacteristics = paginator.page(1)
    except EmptyPage:
        oursamplecharacteristics = paginator.page(paginator.num_pages)    
    
    return render(request, 'visualize/oursamplecharacteristics.html', {'oursamplecharacteristics':oursamplecharacteristics, 'oursamplecharacteristics_fields':oursamplecharacteristics_fields})


@login_required(login_url="/accounts/login")
def pruebatabla(request):
    table = SampleTable(Sample.objects.all())
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50)
    
    return render(request,'visualize/pruebatabla.html', {'table':table})