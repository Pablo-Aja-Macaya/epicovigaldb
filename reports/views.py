from django.shortcuts import render
from .models import Report

# Create your views here.
def get_report_list(request):
    data = Report.objects.all().order_by('fecha_inicial').reverse()
    return render(request, 'reports/reports_list.html', {'data':data})

def get_monthly_report(request, id):
    data = Report.objects.filter(id=id)
    return render(request, 'reports/report.html', {'data':data})

def get_general_report(request, fecha_inicial, fecha_final):
    data = [{'fecha_inicial':fecha_inicial, 'fecha_final':fecha_final}]
    return render(request, 'reports/general_report.html', {'data':data})