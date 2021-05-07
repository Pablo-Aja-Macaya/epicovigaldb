from django.shortcuts import render
from .models import Report
from .ayudantes import get_report_urls


# VIEWS
def get_report_list(request):
    generales = Report.objects.filter(tipo='general').order_by('fecha_inicial').reverse()
    mensuales = Report.objects.filter(tipo='mensual').order_by('fecha_inicial').reverse()
    if request.user.is_authenticated:
        privados = Report.objects.filter(tipo='privado').order_by('fecha_inicial').reverse()
    else:
        privados = None
    context = {
        'generales':generales,
        'mensuales':mensuales,
        'privados':privados
        }
    return render(request, 'reports/reports_list.html', context)

def get_report(request, id):
    data = Report.objects.filter(id=id)
    
    obj = data[0]
    tipo = obj.tipo
    urls_dicc = get_report_urls(obj)

    context = {
        'data':data,
        **urls_dicc
        }

    if tipo=='privado': 
        if request.user.is_authenticated:
            return render(request, 'reports/report.html', context)
        else:
            return render(request, '403.html')
    else:
        return render(request, 'reports/report.html', context)
    