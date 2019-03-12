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
from ActivityModel import index, downloads, about, project, view, services, projects

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.index),
    path('index_site/', index.index_site, name='index_site'),

    path('projects/', projects.projects),
    path('projects/test_sign/', projects.test_sign),
    path('projects/test_login/', projects.test_login),
    path('projects/test_problem/', projects.test_problem),
    path('projects/test_force/', projects.test_force),
    path('projects/test_upload/', projects.test_upload),
    path('projects/file_generation/', projects.file_generation),

    path('projects/analytics/', project.analytice),
    path('projects/export/', project.export),
    path('projects/reports/', project.reports),

    path('services/', services.services),
    path('services_ajax/', services.services_ajax, name='services_ajax'),

    path('downloads/', downloads.downloads),
    path('about/', about.about),

    path('test/', view.gauge),
]
