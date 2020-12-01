from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Region, Sample
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required(login_url="/accounts/login")
def regions(request):

    region_fields = Region._meta.get_fields()
    regions = Region.objects.order_by('location','cp').all()
    page = request.GET.get('page', 1)
    paginator = Paginator(regions, 100)    
    
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
    paginator = Paginator(samples, 100)
    
    try:
        samples = paginator.page(page)
    except PageNotAnInteger:
        samples = paginator.page(1)
    except EmptyPage:
        samples = paginator.page(paginator.num_pages)    
    
    return render(request, 'visualize/samples.html', {'samples':samples, 'sample_fields':sample_fields})