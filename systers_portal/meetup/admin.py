from django.contrib import admin

from meetup.models import MeetupLocation, Meetup


admin.site.register(MeetupLocation)
admin.site.register(Meetup)
