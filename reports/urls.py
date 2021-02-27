# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.tmp, name='report_list'),
    path('all/<str:id>/', views.tmp2, name='report'),
]