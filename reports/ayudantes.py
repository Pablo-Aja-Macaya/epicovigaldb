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

    url_origen = reverse('hospital_graph',args=[obj.encrypted_url_code])
    url_linajes_hospital = reverse('linajes_hospitales_graph',args=[obj.encrypted_url_code])
    url_linajes = reverse('linajes_porcentaje_total',args=[obj.encrypted_url_code])
    url_concellos = reverse('concellos_gal_graph',args=[obj.encrypted_url_code]) 
    url_variants_column_graph = reverse('variants_column_graph',args=[obj.encrypted_url_code])

    urls_dicc = {
        'url_origen' : url_origen,
        'url_linajes_hospital' : url_linajes_hospital,
        'url_linajes' : url_linajes,
        'url_concellos' : url_concellos,        
        'url_variants_column_graph' : url_variants_column_graph
    }
    return urls_dicc
    