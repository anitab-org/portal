from django.conf.urls import url

from meetup.views import MeetupLocationAboutView, MeetupLocationList


urlpatterns = [
    url(r'^(?P<slug>\w+)/about/$', MeetupLocationAboutView.as_view(),
        name='about_meetup_location'),
    url(r'locations/$', MeetupLocationList.as_view(), name='list_meetup_location'),
]
