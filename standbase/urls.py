from django.conf.urls import patterns, url

from standbase import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # url(r'^signup$', views.signup_page, name='signup-page'),
    # url(r'^signup_success$', views.signup_success, name='signup-success'),

    # url(r'^sms_catcher$', views.sms_catcher, name='sms-catcher'),

    # url(r'^trigger_walk$', views.trigger_walk, name='trigger-walk'),
)