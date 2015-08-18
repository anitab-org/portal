from django.contrib import admin

from meetup.models import MeetupLocation, Meetup, Rsvp


admin.site.register(MeetupLocation)
admin.site.register(Meetup)
admin.site.register(Rsvp)
