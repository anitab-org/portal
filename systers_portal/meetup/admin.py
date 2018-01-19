from django.contrib import admin

from meetup.models import MeetupLocation, Meetup, Rsvp, SupportRequest, RequestMeetup


admin.site.register(MeetupLocation)
admin.site.register(Meetup)
admin.site.register(Rsvp)
admin.site.register(SupportRequest)
admin.site.register(RequestMeetup)
