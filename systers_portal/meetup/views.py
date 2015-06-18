from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from meetup.mixins import MeetupLocationMixin
from meetup.models import Meetup, MeetupLocation


class MeetupLocationAboutView(MeetupLocationMixin, TemplateView):
    """Meetup Location about view, show about description of Meetup Location"""
    model = MeetupLocation
    template_name = "meetup/about.html"

    def get_meetup_location(self):
        return get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])


class MeetupLocationList(ListView):
    template_name = "meetup/list_location.html"
    model = MeetupLocation
    paginate_by = 20


class MeetupView(MeetupLocationMixin, DetailView):
    template_name = "meetup/meetup.html"
    model = MeetupLocation

    def get_context_data(self, **kwargs):
        context = super(MeetupView, self).get_context_data(**kwargs)
        context['meetup'] = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'],
                                              meetup_location=self.object)
        return context

    def get_meetup_location(self):
        return self.object


class MeetupLocationMembersView(MeetupLocationMixin, DetailView):
    """Meetup Location members view, show members list of Meetup Location"""
    model = MeetupLocation
    template_name = "meetup/members.html"
    paginate_by = 50

    def get_meetup_location(self):
        return get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
