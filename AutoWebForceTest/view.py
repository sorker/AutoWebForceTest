# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse
import json

def index(request):
    return render(request, 'base/../templates/index.html')


def dashboard(request):
    return render(request, 'base/dashboard.html')


