# -*- coding: utf-8 -*-
from django.urls import path
from jobstatus import views

urlpatterns = [
    path('check', views.check, name='check')
]