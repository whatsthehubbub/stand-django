from django.shortcuts import render, redirect
# from django import forms
from django.http import HttpResponse

from standbase.models import *

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


import logging
logger = logging.getLogger('testlogger')

    
def index(request):
    return render(request, 'standbase/index.html', {
        
    })


@csrf_exempt
@require_POST
def catch(request):
	lat = float(request.POST.get('lat', ''))
	lon = float(request.POST.get('lon', ''))

	vendorid = request.POST.get('vendorid', '')

	s = StandSession.objects.create(lat=lat, lon=lon, vendorid=vendorid)

	return HttpResponse('%d' % s.id)