from .models import Report
from django.urls import reverse

# Funciones de ayuda
def get_report_urls(obj):
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

    urls_dicc = {
        'url_origen' : url_origen,
        'url_linajes_hospital' : url_linajes_hospital,
        'url_linajes' : url_linajes,
        'url_concellos' : url_concellos,        
    }
    return urls_dicc
    