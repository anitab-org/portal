from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from meetup.models import MeetupLocation


class MeetupLocationDetailView(DetailView):
    """Meetup Location page view, show only details that user requested"""
    model = MeetupLocation


class MeetupLocationListView(ListView):
    """ List all Meetup Locations"""
    model = MeetupLocation
