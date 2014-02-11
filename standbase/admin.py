from django.contrib import admin

from standbase.models import *

class StandSessionAdmin(admin.ModelAdmin):
    list_display = ('lat', 'lon', 'message', 'vendorid', 'venueid')

admin.site.register(StandSession, StandSessionAdmin)