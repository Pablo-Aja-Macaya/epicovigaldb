from django.shortcuts import render
from .models import Report
from django.urls import reverse

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
    
    obj = data[0]
    fecha_inicial = obj.fecha_inicial
    fecha_final = obj.fecha_final
    tipo = obj.tipo
    categoria = obj.categoria
    umbral = getattr(obj, 'umbral', None)
    filtro = getattr(obj, 'filtro', None)

    ## Enlaces para gráficas
    args = [fecha_inicial,fecha_final,categoria]
    args_sin_umbral = args.copy()
    args_con_umbral = args.copy()

    if umbral:
        args_con_umbral.append(umbral)
    if filtro:
        args_sin_umbral.append(filtro)
        args_con_umbral.append(filtro)

    url_origen = reverse('hospital_graph',args=args_sin_umbral)
    url_linajes_hospital = reverse('linajes_hospitales_graph',args=args_con_umbral)
    url_linajes = reverse('linajes_porcentaje_total',args=args_con_umbral)
    url_concellos = reverse('concellos_gal_graph',args=args_sin_umbral) 

    context = {
        'data':data,
        'url_origen' : url_origen,
        'url_linajes_hospital' : url_linajes_hospital,
        'url_linajes' : url_linajes,
        'url_concellos' : url_concellos,
        }
    if tipo=='privado': 
        if request.user.is_authenticated:
            return render(request, 'reports/report.html', context)
        else:
            return render(request, '403.html')
    else:
        return render(request, 'reports/report.html', context)
    