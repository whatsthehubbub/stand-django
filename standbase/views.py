from django.shortcuts import render, redirect
# from django import forms
from django.http import HttpResponse

from standbase.models import *

from django.views.decorators.csrf import csrf_exempt


import logging
logger = logging.getLogger('testlogger')


def index(request):
    return render(request, 'standbase/index.html', {
        
    })