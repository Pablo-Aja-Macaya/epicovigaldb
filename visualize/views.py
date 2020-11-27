from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from upload.models import Region

@login_required(login_url="/accounts/login")
def regions(request):
    i = 0
    n = 100
    regions = Region.objects.all()[i:i+n]
    return render(request, 'visualize/regions.html', {'regions':regions})