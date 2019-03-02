# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse
import json


def index(request):
    return render(request, 'index.html')


def project(request):
    return render(request, 'project.html')


def services(request):
    return render(request, 'services.html')


def downloads(request):
    return render(request, 'downloads.html')


def about(request):
    return render(request, 'about.html')
