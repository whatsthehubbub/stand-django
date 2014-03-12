from django.conf.urls import patterns, url

from standbase import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^catch$', views.catch, name='catch'),
    url(r'^done$', views.done, name='done'),
    url(r'^live$', views.live, name='live'),

    url(r'^s/(?P<sessionid>\d+)/$', views.session, name='session'),
    url(r'^for/(?P<topic_slug>\D+)/$', views.topic, name='topic'),

    # url(r'^signup_success$', views.signup_success, name='signup-success'),

    # url(r'^sms_catcher$', views.sms_catcher, name='sms-catcher'),

    # url(r'^trigger_walk$', views.trigger_walk, name='trigger-walk'),
)