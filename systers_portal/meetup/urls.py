from django.conf.urls import url

from meetup.views import MeetupLocationDetailView, MeetupLocationListView


urlpatterns = [
    url(r'^locations$', MeetupLocationListView.as_view(), name='list_all_meetup_locations'),
    url(r'^(?P<slug>\w+)/upcoming/$',
        MeetupLocationDetailView.as_view(template_name='meetup/upcoming.html'),
        name='upcoming_meetup_location'),
    url(r'^(?P<slug>\w+)/past/$',
        MeetupLocationDetailView.as_view(template_name='meetup/past.html'),
        name='past_meetup_location'),
    url(r'^(?P<slug>\w+)/about/$',
        MeetupLocationDetailView.as_view(template_name='meetup/about.html'),
        name='about_meetup_location'),
    url(r'^(?P<slug>\w+)/organizers/$',
        MeetupLocationDetailView.as_view(template_name='meetup/organizers.html'),
        name='organizers_meetup_location'),
    url(r'^(?P<slug>\w+)/members/$',
        MeetupLocationDetailView.as_view(template_name='meetup/all_members.html'),
        name='all_members_meetup_location'),
    url(r'^(?P<slug>\w+)/sponsors/$',
        MeetupLocationDetailView.as_view(template_name='meetup/sponsors.html'),
        name='sponsors_meetup_location'),
]
