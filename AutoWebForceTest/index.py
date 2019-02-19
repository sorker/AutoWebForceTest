# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render


context = {}

def hello(request):
    # return HttpResponse('hello')
    return render(request, 'bootstrapmodel.html', context)
