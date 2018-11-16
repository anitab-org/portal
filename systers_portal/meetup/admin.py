from django.contrib import admin

from meetup.models import (Meetup, MeetupLocation, Rsvp, SupportRequest, RequestMeetupLocation,
                           RequestMeetup)


admin.site.register(MeetupLocation)
admin.site.register(Meetup)
admin.site.register(Rsvp)
admin.site.register(SupportRequest)
admin.site.register(RequestMeetup)
admin.site.register(RequestMeetupLocation)
