from django.contrib import admin

from medux.plugins.timetracker.models import TimeEntry, Holiday

admin.site.register(TimeEntry)
admin.site.register(Holiday)
