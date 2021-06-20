from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django_tables2 import RequestConfig


# Create your views here.
@login_required(login_url="/accounts/login")
def check(request):
    table = StatusTable(Status.objects.all().order_by('-fecha'))
    RequestConfig(request).configure(table)
    table.paginate(page=request.GET.get("page", 1), per_page=50) 

    prev_url = request.META.get('HTTP_REFERER')

    context = {'table':table, 'prev_url':prev_url}
    return render(request, 'jobstatus/status.html', context)