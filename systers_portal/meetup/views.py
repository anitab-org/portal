from django.views.generic.detail import DetailView

from meetup.models import MeetupLocation


class MeetupLocationAboutView(DetailView):
    """Meetup Location about view, show about description of Meetup Location"""
    model = MeetupLocation
    template_name = "meetup/about.html"
