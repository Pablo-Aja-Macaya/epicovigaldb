from django.shortcuts import render
from .models import Report

# Create your views here.
def get_report_list(request):
    data = Report.objects.all().order_by('fecha_inicial').reverse()
    return render(request, 'reports/reports_list.html', {'data':data})

def get_report(request, id):
    data = Report.objects.filter(id=id)
    return render(request, 'reports/report.html', {'data':data})