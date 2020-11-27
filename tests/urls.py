# -*- coding: utf-8 -*-
from django.urls import path
from tests import views

urlpatterns = [
    path('selection', views.tests, name='selection'),
]