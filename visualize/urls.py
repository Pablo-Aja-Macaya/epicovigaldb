# -*- coding: utf-8 -*-

from django.urls import path
from visualize import views

urlpatterns = [
    path('regions', views.regions, name='regions'),
    path('samples', views.samples, name='samples'),
]