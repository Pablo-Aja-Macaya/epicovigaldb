# -*- coding: utf-8 -*-
from django.urls import path
from tests import views

urlpatterns = [
    path('selection', views.tests, name='selection'),
    path('upload_test_results', views.upload_test_results, name='upload_test_results'),
    path('update', views.update_from_folder, name='update'),
    path('send_selection', views.send_selection, name='send_selection'),
    path('send_results', views.send_results, name='send_results'),
    path('test_errors', views.test_errors, name='test_errors'),
]