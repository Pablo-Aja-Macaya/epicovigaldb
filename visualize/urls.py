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
]