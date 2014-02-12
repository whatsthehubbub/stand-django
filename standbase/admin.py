from django.contrib import admin

from standbase.models import *

class StandSessionAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'datefinished', 'lat', 'lon', 'secret', 'message', 'vendorid', 'venueid')

admin.site.register(StandSession, StandSessionAdmin)