from django.shortcuts import render
from .models import Report

# Create your views here.
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

# def get_monthly_report(request, id):
#     data = Report.objects.filter(id=id, tipo='mensual')
#     return render(request, 'reports/report.html', {'data':data})

# def get_general_report(request, fecha_inicial, fecha_final):
#     data = [{'fecha_inicial':fecha_inicial, 'fecha_final':fecha_final}]
#     return render(request, 'reports/general_report.html', {'data':data})

def get_report(request, id):
    data = Report.objects.filter(id=id)
    if data.values('tipo')[0]['tipo']=='privado': 
        if request.user.is_authenticated:
            return render(request, 'reports/report.html', {'data':data})
        else:
            return render(request, '403.html')
    else:
        return render(request, 'reports/report.html', {'data':data})
    