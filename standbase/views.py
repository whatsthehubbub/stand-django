from django.shortcuts import render, redirect
# from django import forms
from django.http import HttpResponse

from standbase.models import *

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.utils import timezone

import json
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

	response = {
		'sessionid': s.id,
		'secret': s.secret
	}
	return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
@require_POST
def done(request):
	secret = request.POST.get('secret', '')
	sessionid = request.POST.get('sessionid', '')
	duration = request.POST.get('duration', 0)
	# TODO the request will probably come a bit later than it is actually finished

	s = StandSession.objects.get(secret=secret, id=sessionid)

	s.datefinished = s.datecreated + datetime.timedelta(seconds=duration)

	s.save()

	response = {
		'status': 1
	}

	return HttpResponse(json.dumps(response), content_type='application/json')

