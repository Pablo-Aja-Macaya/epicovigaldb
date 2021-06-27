# -*- coding: utf-8 -*-

from django.urls import path
from visualize import views

urlpatterns = [
    path('general', views.general, name='general'),
    path('edit/<str:id_uvigo>+<str:tipo>', views.edit_form, name='edit_form'),
    path('drop', views.drop_sample_cascade, name='drop_sample'),
    path('sample/<str:id_uvigo>', views.specific_sample, name='specific_sample'),
    path('region/<str:id_region>', views.specific_region, name='specific_region'),
    # Metadatos
    path('regions', views.regions, name='regions'),
    path('samples', views.samples, name='samples'),
    path('metadata', views.metadata, name='oursamplecharacteristics'),
    # Resultados
    path('picard', views.picard, name='picard'),
    path('nextclade', views.nextclade, name='nextclade'),
    path('ngsstats', views.ngsstats, name='ngsstats'),
    path('singlecheck', views.singlecheck, name='singlecheck'),
    path('variants', views.variants, name='variants'),
    path('lineages', views.lineages, name='lineages'),
    # Graficas
    path('graphs/', views.get_graphs, name="get_graphs"),
        # Proporción por hospital
        path('hospital_graph/<str:encrypted_url_code>', views.hospital_graph, name="hospital_graph"),
        # Muestras por concello
        path('concellos_gal_graph/<str:encrypted_url_code>', views.concellos_gal_graph, name="concellos_gal_graph"),
        # Linajes por hospital
        path('linajes_hospitales_graph/<str:encrypted_url_code>', views.linajes_hospitales_graph, name="linajes_hospitales_graph"),
        # Cantidad total de cada linaje
        path('linajes_porcentaje_total/<str:encrypted_url_code>', views.linajes_porcentaje_total, name="linajes_porcentaje_total"),
        # Proporción de variantes en cada época
        path('variants_column_graph/<str:encrypted_url_code>', views.variants_column_graph, name="variants_column_graph"),

        # Sin usar
        path('variants_line_graph/<str:fecha_inicial>+<str:fecha_final>/<str:variant>', views.variants_line_graph, name="variants_line_graph"),
]