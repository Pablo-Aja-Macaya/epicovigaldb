# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_report_list, name='report_list'),
    path('all/monthly/<str:id>/', views.get_monthly_report, name='report'),
    path('all/general/<str:fecha_inicial>+<str:fecha_final>', views.get_general_report, name='general_report')
]