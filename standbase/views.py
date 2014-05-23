from django.shortcuts import render, redirect
# from django import forms
from django.http import HttpResponse, HttpResponseNotFound

from standbase.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Count

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page

from django.utils import timezone
from django.utils.text import slugify
from django.utils.cache import add_never_cache_headers

import datetime
import json
import string

import logging
logger = logging.getLogger('testlogger')

def expire_view_cache(view_name, args=[], namespace=None, key_prefix=None):
    """
    This function allows you to invalidate any view-level cache. 
        view_name: view function you wish to invalidate or it's named url pattern
        args: any arguments passed to the view function
        namepace: optioal, if an application namespace is needed
        key prefix: for the @cache_page decorator for the function (if any)

    from: http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
    """
    from django.core.urlresolvers import reverse
    from django.http import HttpRequest
    from django.utils.cache import get_cache_key
    from django.core.cache import cache
    # create a fake request object
    request = HttpRequest()
    # Loookup the request path:
    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args)
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):
            # Delete the cache entry.  
            #
            # Note that there is a possible race condition here, as another 
            # process / thread may have refreshed the cache between
            # the call to cache.get() above, and the cache.set(key, None) 
            # below.  This may lead to unexpected performance problems under 
            # severe load.
            cache.set(key, None, 0)
        return True
    return False

from django.db.models.signals import post_save

def invalidate_api_state(sender, **kwargs):
    expire_view_cache('api_state')

post_save.connect(invalidate_api_state, sender=StandSession)
post_save.connect(invalidate_api_state, sender=Topic)


def get_active_sessions():
    # Active are sessions without a date finished
    # But with a live call within the last five minutes
    return StandSession.objects.filter(datefinished=None).filter(datelive__gt=timezone.now()-datetime.timedelta(seconds=300)).order_by('-datecreated')

def get_completed_sessions():
    return StandSession.public_objects.exclude(datefinished=None).order_by('-datefinished')[:10]

def index(request):
    return render(request, 'standbase/index.html', {
        'active_sessions': get_active_sessions(),
        'completed_sessions': get_completed_sessions(),
        'trending_topics': Topic.public_objects.exclude(slug='something').annotate(Count('standsession')).order_by('-standsession__count')[:5],
        'total_time': formatted_duration(StandSession.objects.all().aggregate(Sum('duration'))['duration__sum'])
    })

def now(request):
    return render(request, 'standbase/now.html', {

    })

# This is cached for four minutes max
# Cache is invalidated on write to any object, so it should be always up to date
@cache_page(60 * 4)
def api_state(request):
    # .values('id', 'datecreated', 'lat', 'lon', 'datelive', 'datefinished', 'topic__name', 'parsed_geocode')
    response = {
        'active_sessions': [{
            'id': s.id,
            'datecreated': s.datecreated,
            'lat': s.lat,
            'lon': s.lon,
            'datelive': s.datelive,
            'datefinished': s.datefinished,
            'topic__name': s.topic.public and s.topic.name or 'something',
            'parsed_geocode': s.parsed_geocode()
        } for s in get_active_sessions()],
        'completed_sessions': [{
            'id': s.id,
            'datecreated': s.datecreated,
            'lat': s.lat,
            'lon': s.lon,
            'datelive': s.datelive,
            'datefinished': s.datefinished,
            'topic__name': s.topic.name,
            'parsed_geocode': s.parsed_geocode(),
            'get_absolute_url': s.get_absolute_url(),
        } for s in get_completed_sessions()]
    }

    # However we don't want the client to cache this page ever
    response = HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

    add_never_cache_headers(response)

    return response

def session(request, sessionid):
    try:
        s = StandSession.objects.get(id=sessionid)

        if s.datefinished:
            return render(request, 'standbase/stand.html', {
                's': s,
                'total_time': formatted_duration(StandSession.objects.all().aggregate(Sum('duration'))['duration__sum'])
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
            'sessions': sessions,
            'total_time': formatted_duration(StandSession.objects.all().aggregate(Sum('duration'))['duration__sum'])
        })
    except Topic.DoesNotExist:
        return HttpResponseNotFound("Couldn't find such a topic.")


@require_POST
@csrf_exempt
def catch(request):
    lat = float(request.POST.get('lat', ''))
    lon = float(request.POST.get('lon', ''))

    vendorid = request.POST.get('vendorid', '')

    message = request.POST.get('message', 'something')
    slug = slugify(message)
    try:
        topic = Topic.objects.get(slug=slug)
    except Topic.DoesNotExist:
        topic = Topic.objects.create(name=message, slug=slug)

    s = StandSession.objects.create(lat=lat, lon=lon, vendorid=vendorid, datelive=timezone.now(), topic=topic)

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

    # TODO done does not check if the live is within a reasonable time ago
    try:
        s = StandSession.objects.get(secret=secret, id=sessionid)

        if 'duration' in request.POST:
            duration = int(request.POST.get('duration', '0'))

            s.duration = duration
            s.datefinished = s.datecreated + datetime.timedelta(seconds=duration)

        s.save()

        code = 1
    except StandSession.DoesNotExist:
        code = 0

    response = {
        'status': code
    }

    return HttpResponse(json.dumps(response), content_type='application/json')

