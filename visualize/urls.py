# -*- coding: utf-8 -*-

from django.urls import path
from visualize import views

urlpatterns = [
    path('general', views.general, name='general'),
    path('edit/<str:id_uvigo>+<str:tipo>', views.edit_form, name='edit_form'),
    path('drop', views.drop_sample_cascade, name='drop_sample'),
    path('sample/<str:id_uvigo>', views.specific_sample, name='specific_sample'),
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
        ## Proporción por hospital
        path('hospital_graph/<str:fecha_inicial>+<str:fecha_final>', views.hospital_graph, name="hospital_graph"),
        path('hospital_graph/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>', views.hospital_graph, name="hospital_graph"),
        path('hospital_graph/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>/<str:filtro>', views.hospital_graph, name="hospital_graph"),
        ## Muestras por concello
        path('concellos_gal_graph/<str:fecha_inicial>+<str:fecha_final>', views.concellos_gal_graph, name="concellos_gal_graph"),
        path('concellos_gal_graph/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>', views.concellos_gal_graph, name="concellos_gal_graph"),    
        path('concellos_gal_graph/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>/<str:filtro>', views.concellos_gal_graph, name="concellos_gal_graph"),
        ## Linajes por hospital
        path('linajes_hospitales_graph/<str:fecha_inicial>+<str:fecha_final>', views.linajes_hospitales_graph, name="linajes_hospitales_graph"),
        path('linajes_hospitales_graph/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>', views.linajes_hospitales_graph, name="linajes_hospitales_graph"),
        path('linajes_hospitales_graph/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>/<str:filtro>', views.linajes_hospitales_graph, name="linajes_hospitales_graph"),
        ## Cantidad total de cada linaje
        path('linajes_porcentaje_total/<str:fecha_inicial>+<str:fecha_final>', views.linajes_porcentaje_total, name="linajes_porcentaje_total"),
        path('linajes_porcentaje_total/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>', views.linajes_porcentaje_total, name="linajes_porcentaje_total"),
        path('linajes_porcentaje_total/<str:fecha_inicial>+<str:fecha_final>/<str:categoria>/<str:filtro>', views.linajes_porcentaje_total, name="linajes_porcentaje_total"),

        # Sin usar
        path('variants_line_graph/<str:fecha_inicial>+<str:fecha_final>/<str:variant>', views.variants_line_graph, name="variants_line_graph"),
        path('variants_column_graph/<str:fecha_inicial>+<str:fecha_final>/<str:variant>', views.variants_column_graph, name="variants_column_graph"),
]