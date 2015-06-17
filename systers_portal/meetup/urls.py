from django.conf.urls import url

from meetup.views import MeetupLocationAboutView


urlpatterns = [
    url(r'^(?P<slug>\w+)/about/$', MeetupLocationAboutView.as_view(),
        name='about_meetup_location'),
]
