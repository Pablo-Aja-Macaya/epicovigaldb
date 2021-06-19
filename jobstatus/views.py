from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
# @login_required(login_url="/accounts/login")
# def check(request):
#     status_fields = Status._meta.get_fields()
#     status = Status.objects.order_by('-date').all()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(status, 10)
    
#     try:
#         status = paginator.page(page)
#     except PageNotAnInteger:
#         status = paginator.page(1)
#     except EmptyPage:
#         status = paginator.page(paginator.num_pages)    
    
#     return render(request, 'jobstatus/status.html', {'status':status, 'status_fields':status_fields})