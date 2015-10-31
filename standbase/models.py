from django.db import models
from django.db.models import Sum

# from django.db.models import Q

from django.core.urlresolvers import reverse
from django.utils import timezone

import json
import random
import urllib2, urllib
from xml.dom import minidom

import logging
logger = logging.getLogger('testlogger')

def list_duration(d):
    days = d / (24 * 60 * 60)
    d -= days * 24 * 60 * 60

    hours = d / (60 * 60)
    d -= hours * 60 * 60

    minutes = d / 60
    d -= minutes * 60

    seconds = d

    returnValue = []
    if days > 1:
        returnValue.append('%d days' % days)
    elif days > 0:
        returnValue.append('1 day')

    if hours > 1:
        returnValue.append('%d hours' % hours)
    elif hours > 0:
        returnValue.append('1 hour')

    if minutes > 1:
        returnValue.append('%d minutes' % minutes)
    elif minutes > 0:
        returnValue.append('1 minute')

    if seconds > 1:
        returnValue.append('%d seconds' % seconds)
    elif seconds > 0:
        returnValue.append('1 second')

    return returnValue

def formatted_duration(d):
    returnValue = list_duration(d)

    returnString = []
    for counter in range(len(returnValue)):
        returnString.append(returnValue[counter])

        if counter < len(returnValue)-2:
            returnString.append(', ')
        elif counter < len(returnValue)-1:
            returnString.append(' and ')

    return ''.join(returnString)


class PublicSessionManager(models.Manager):
    def get_queryset(self):
        return super(PublicSessionManager, self).get_queryset().filter(topic__public=True)

class StandSession(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    # Location
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    # Used to later update this model
    secret = models.CharField(max_length=255, default=lambda: ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(50)]))

    datelive = models.DateTimeField(blank=True, null=True)
    datefinished = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(default=0)

    # Topic
    topic = models.ForeignKey('Topic', blank=True, null=True)

    objects = models.Manager()
    public_objects = PublicSessionManager()

    # Vendorid
    # http://www.doubleencore.com/2013/04/unique-identifiers/
    vendorid = models.CharField(max_length=255)

    # What the reverse geocode comes up with for this location
    geocode = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('session', args=[self.id])

    def retrieve_reverse_geocode(self):
        url = 'http://api.geonames.org/extendedFindNearby?lat=%f&lng=%f&username=alper' % (self.lat, self.lon)
        urlcon = urllib2.urlopen(url)

        self.geocode = urlcon.read()
        self.save()
        print 'retrieved reverse'

    def post_to_slack(self):
        # This is a secret URL. If ever we open source this, we should change this.
        webhook_url = 'https://hubbub.slack.com/services/hooks/incoming-webhook?token='

        payload = {'text': 'A session was just completed with duration %d about "%s" (%s), see it here: <http://getstanding.com%s>' % (self.duration, self.topic.name, self.topic.public and 'public' or 'private', self.get_absolute_url())}
        data = {'payload': json.dumps(payload)}

        urlcon = urllib2.urlopen(webhook_url, urllib.urlencode(data))
        urlcon.close()


    def parsed_geocode(self):
        def getText(nodelist):
            rc = []
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc.append(node.data)
            return ''.join(rc)

        def getGeoNameWithCode(geonames, code):
            for geoname in geonames:
                fcode = getText(geoname.getElementsByTagName('fcode')[0].childNodes)

                if fcode == code:
                    result = getText(geoname.getElementsByTagName('name')[0].childNodes)

                    return result
            return ''

        if self.geocode:
            xmldoc = minidom.parseString(self.geocode.encode('utf-8'))
            geonames = xmldoc.getElementsByTagName('geoname')

            if geonames:
                localarea = getGeoNameWithCode(geonames, 'PPLX')
                if not localarea:
                    localarea = getGeoNameWithCode(geonames, 'PPLH')

                city = getGeoNameWithCode(geonames, 'ADM4')
                if not city:
                    city = getGeoNameWithCode(geonames, 'ADM2')
            else:
                # In some cases there will be no geoname blocks but address information
                # will be in a single <geonames> block and we need to get it from there
                placename = xmldoc.getElementsByTagName('placename')

                localarea = None

                if placename:
                    city = getText(placename[0].childNodes)
                else:
                    # Sometimes we get absolutely nothing back from geonames
                    # In that case we jus get the first <name> element and its contents
                    city = getText(xmldoc.getElementsByTagName('name')[0].childNodes)

            """
            Another degenerate example:
            <?xml version="1.0" encoding="UTF-8" standalone="no"?>
<geonames>
<ocean>
<name>North Sea</name>
</ocean>
</geonames>
            """

            return (localarea, city)
        else:
            return None

    def rendered_geocode(self):
        pieces = self.parsed_geocode()

        if not (pieces[0] or pieces[1]):
            # Both empty
            return ''
        elif not pieces[0]:
            return pieces[1]
        elif not pieces[1]:
            return pieces[0]
        else:
            return '%s, %s' % (pieces[0], pieces[1])

    def update_duration(self):
        if self.duration == 0 and self.datefinished:
            d = self.datefinished - self.datecreated

            self.duration = d.total_seconds()
            self.save()

        return self.duration

    def get_duration(self):
        return formatted_duration(self.duration)

    def live_duration(self):
        """Method we need for active sessions because they don't have a duration filled in yet."""
        seconds = (timezone.now() - self.datecreated).total_seconds()

        return formatted_duration(int(seconds))


class PublicTopicManager(models.Manager):
    def get_queryset(self):
        return super(PublicTopicManager, self).get_queryset().filter(public=True)

class Topic(models.Model):
    datecreated = models.DateTimeField(auto_now_add=True)
    datechanged = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    public = models.BooleanField(default=False)

    objects = models.Manager()
    public_objects = PublicTopicManager()

    def get_absolute_url(self):
        return reverse('topic', args=[self.slug])

    def get_total_duration(self):
        result = self.standsession_set.all().aggregate(Sum('duration'))

        duration = result['duration__sum']

        return formatted_duration(duration)

    def __unicode__(self):
        return self.name