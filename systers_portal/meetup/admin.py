from django.contrib import admin

from meetup.models import (Meetup, Rsvp, SupportRequest, RequestMeetup)

admin.site.register(Meetup)
admin.site.register(Rsvp)
admin.site.register(SupportRequest)
admin.site.register(RequestMeetup)
