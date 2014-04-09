from django.contrib import admin

from standbase.models import *

class StandSessionAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'datefinished', 'lat', 'lon', 'secret', 'topic', 'vendorid')
    list_filter = ('topic__public', )

admin.site.register(StandSession, StandSessionAdmin)


def make_public(modeladmin, request, queryset):
	queryset.update(public=True)
make_public.short_description = "Make topics public"

class TopicAdmin(admin.ModelAdmin):
    list_display = ('datecreated', 'name', 'public')
    list_filter = ('public', )

    actions = [make_public]

admin.site.register(Topic, TopicAdmin)