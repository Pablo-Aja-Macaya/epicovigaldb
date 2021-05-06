"""epicovigal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks import views
from django.views.static import serve
from django.conf.urls import url
urlpatterns = [
    path('administrador/epicovigal/', admin.site.urls),
    path('', views.home, name="home"),
    path('consorcio', views.consorcio, name="consorcio"),
    #url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    
    # Apps
    path('accounts/', include('accounts.urls')),
    path('upload/', include('upload.urls')),
    path('tests/', include('tests.urls')),
    path('reports/', include('reports.urls')),
    path('visualize/', include('visualize.urls')),
    path('jobstatus/', include('jobstatus.urls')),
    path('nextstrain/', include('nextstrainApp.urls')),
    path('microreact/', include('microreact.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
