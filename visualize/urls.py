# -*- coding: utf-8 -*-

from django.urls import path
from visualize import views

urlpatterns = [
    path('general', views.general, name='general'),
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
    path('hospital_graph/<str:fecha_inicial>+<str:fecha_final>', views.hospital_graph, name="hospital_graph"),
    path('variants_line_graph/<str:fecha_inicial>+<str:fecha_final>/<str:variant>', views.variants_line_graph, name="variants_line_graph"),
    path('variants_column_graph/<str:fecha_inicial>+<str:fecha_final>/<str:variant>', views.variants_column_graph, name="variants_column_graph"),
    path('concellos_gal_graph/<str:fecha_inicial>+<str:fecha_final>', views.concellos_gal_graph, name="concellos_gal_graph"),
    path('linajes_hospitales_graph/<str:fecha_inicial>+<str:fecha_final>', views.linajes_hospitales_graph, name="linajes_hospitales_graph"),
]