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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),

    # Gráficas
    path('hospital_graph/', views.hospital_graph, name="hospital_graph"),
    path('variants_line_graph/<str:fecha>/<str:variant>', views.variants_line_graph, name="variants_line_graph"),
    path('variants_column_graph/<str:fecha>/<str:variant>', views.variants_column_graph, name="variants_column_graph"),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('upload/', include('upload.urls')),
    path('tests/', include('tests.urls')),
    path('visualize/', include('visualize.urls')),
    path('jobstatus/', include('jobstatus.urls')),
    path('nextstrain/', include('nextstrainApp.urls')),
    path('microreact/', include('microreact.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
