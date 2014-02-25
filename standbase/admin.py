from django.contrib import admin

from standbase.models import *

class StandSessionAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'datefinished', 'lat', 'lon', 'secret', 'topic', 'vendorid')

admin.site.register(StandSession, StandSessionAdmin)

class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'public')

admin.site.register(Topic, TopicAdmin)