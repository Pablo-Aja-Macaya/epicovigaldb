# -*- coding: utf-8 -*-


from django.urls import path
from . import views

urlpatterns = [
    path('manual', views.upload_manual, name='manual'),
    path('csv', views.upload_csv, name='csv'),
    path('upload', views.upload, name='upload')
]