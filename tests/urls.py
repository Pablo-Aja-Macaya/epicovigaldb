# -*- coding: utf-8 -*-
from django.urls import path
from tests import views

urlpatterns = [
    path('selection', views.tests, name='selection'),
    path('upload_test_results', views.upload_test_results, name='upload_test_results'),
    path('send_selection', views.send_selection, name='send_selection'),
    path('send_results', views.send_results, name='send_results'),
]