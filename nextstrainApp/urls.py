# -*- coding: utf-8 -*-

from django.urls import path
from nextstrainApp import views

urlpatterns = [
    path('auspice', views.auspice, name='auspice'),
]