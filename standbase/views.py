from django.shortcuts import render, redirect
# from django import forms
from django.http import HttpResponse, HttpResponseNotFound

from standbase.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Count

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.utils import timezone
from django.utils.text import slugify

import datetime
import json
import string

import logging
logger = logging.getLogger('testlogger')


def index(request):
    return render(request, 'standbase/index.html', {
        'active_sessions': StandSession.objects.filter(datefinished=None).filter(datelive__gt=timezone.now()-datetime.timedelta(seconds=300)).order_by('-datecreated'),
        'completed_sessions': StandSession.public_objects.exclude(datefinished=None).order_by('-datefinished')[:10],
        'trending_topics': Topic.public_objects.annotate(Count('standsession')).order_by('-standsession__count')[:5]
    })

def session(request, sessionid):
    try:
        s = StandSession.objects.get(id=sessionid)

        if s.datefinished:
            return render(request, 'standbase/stand.html', {
                's': s
            })
        else:
            return HttpResponseNotFound("Couldn't find such a session.")
    except StandSession.DoesNotExist:
        return HttpResponseNotFound("Couldn't find such a session.")


def topic(request, topic_slug):
    try:
        t = Topic.objects.get(slug=topic_slug, public=True)

        page = request.GET.get('page')

        session_list = StandSession.public_objects.filter(topic=t).exclude(datefinished=None).order_by('-datefinished')
        paginator = Paginator(session_list, 25)

        try:
            sessions = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            sessions = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            sessions = paginator.page(paginator.num_pages)

        return render(request, 'standbase/topic.html', {
            't': t,
            'duration': int(sum([(s.datefinished - s.datecreated).total_seconds() for s in t.standsession_set.exclude(datefinished=None)])),
            'sessions': sessions
        })
    except Topic.DoesNotExist:
        return HttpResponseNotFound("Couldn't find such a topic.")


@require_POST
@csrf_exempt
def catch(request):
    lat = float(request.POST.get('lat', ''))
    lon = float(request.POST.get('lon', ''))

    vendorid = request.POST.get('vendorid', '')

    something, created = Topic.objects.get_or_create(name='something')

    s = StandSession.objects.create(lat=lat, lon=lon, vendorid=vendorid, datelive=timezone.now(), topic=something)

    import django_rq
    django_rq.enqueue(s.retrieve_reverse_geocode)

    response = {
        'sessionid': s.id,
        'secret': s.secret
    }
    return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
@require_POST
def live(request):
    secret = request.POST.get('secret', '')
    sessionid = request.POST.get('sessionid', '')

    try:
        s = StandSession.objects.get(secret=secret, id=sessionid)

        s.datelive = timezone.now()
        s.save()

        code = 1
    except StandSession.DoesNotExist:
        code = 0

    response = {
        'status': code
    }

    return HttpResponse(json.dumps(response), content_type='application/json')

@csrf_exempt
@require_POST
def done(request):
    secret = request.POST.get('secret', '')
    sessionid = request.POST.get('sessionid', '')

    try:
        s = StandSession.objects.get(secret=secret, id=sessionid)

        if 'duration' in request.POST:
            duration = int(request.POST.get('duration', '0'))
            s.datefinished = s.datecreated + datetime.timedelta(seconds=duration)

        # TODO rename to 
        if 'message' in request.POST:
            message = request.POST.get('message', '')

            if message:
                slug = slugify(message)

                try:
                    topic = Topic.objects.get(slug=slug)
                except Topic.DoesNotExist:
                    topic = Topic.objects.create(name=message, slug=slug)

                s.topic = topic

        s.save()

        code = 1
    except StandSession.DoesNotExist:
        code = 0

    response = {
        'status': code
    }

    return HttpResponse(json.dumps(response), content_type='application/json')

