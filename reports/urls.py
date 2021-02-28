# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_report_list, name='report_list'),
    path('all/<str:id>/', views.get_report, name='report'),
]