# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse
import json


def index(request):
    return render(request, 'index.html')


def projects(request):
    return render(request, 'projects.html')


def services(request):
    return render(request, 'services.html')


def downloads(request):
    return render(request, 'downloads.html')


def about(request):
    return render(request, 'about0.html')
