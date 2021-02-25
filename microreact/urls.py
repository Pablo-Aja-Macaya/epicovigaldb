# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('project', views.project, name='microreact'),
]