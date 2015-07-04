from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from meetup.mixins import MeetupLocationMixin
from meetup.models import MeetupLocation


class MeetupLocationAboutView(MeetupLocationMixin, TemplateView):
    """Meetup Location about view, show about description of Meetup Location"""
    model = MeetupLocation
    template_name = "meetup/about.html"

    def get_meetup_location(self):
        return get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
