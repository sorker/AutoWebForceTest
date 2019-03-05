"""AutoWebForceTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path
from . import index, about, projects, services, downloads, view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index),
    path('projects/', projects.projects),
    path('services/', services.services),
    path('downloads/', downloads.downloads),
    path('about/', about.about),
    path('test/', view.gauge),
    path('services_ajax/', services.services_ajax, name='services_ajax'),
    path('index_site/', index.index_site)
]
