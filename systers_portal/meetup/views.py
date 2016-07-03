import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView, TemplateView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages

from meetup.forms import (AddMeetupForm, EditMeetupForm, AddMeetupLocationMemberForm,
                          AddMeetupLocationForm, EditMeetupLocationForm, RsvpForm)
from meetup.mixins import MeetupLocationMixin
from meetup.models import Meetup, MeetupLocation, Rsvp
from users.models import SystersUser


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

    def get_context_data(self, **kwargs):
        context = super(MeetupLocationMembersView, self).get_context_data(**kwargs)
        organizer_list = self.meetup_location.organizers.all()
        context['organizer_list'] = organizer_list
        context['member_list'] = self.meetup_location.members.exclude(id__in=organizer_list)
        return context

    def get_meetup_location(self):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        return self.meetup_location


class AddMeetupView(LoginRequiredMixin, MeetupLocationMixin, CreateView):
    """Add new meetup"""
    template_name = "meetup/add_meetup.html"
    model = Meetup
    form_class = AddMeetupForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_meetup", kwargs={"slug": self.meetup_location.slug,
                                              "meetup_slug": self.object.slug})

    def get_form_kwargs(self):
        """Add request user and meetup location object to the form kwargs.
        Used to autofill form fields with created_by and meetup_location without
        explicitly filling them up in the form."""
        kwargs = super(AddMeetupView, self).get_form_kwargs()
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        kwargs.update({'created_by': self.request.user})
        kwargs.update({'meetup_location': self.meetup_location})
        return kwargs

    def get_meetup_location(self):
        return self.meetup_location


class DeleteMeetupView(LoginRequiredMixin, MeetupLocationMixin, DeleteView):
    """Delete existing Meetup"""
    template_name = "meetup/meetup_confirm_delete.html"
    model = Meetup
    slug_url_kwarg = "meetup_slug"
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful deletion"""
        self.get_meetup_location()
        return reverse("about_meetup_location",
                       kwargs={"slug": self.meetup_location.slug})

    def get_meetup_location(self):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        return self.meetup_location


class EditMeetupView(LoginRequiredMixin, UpdateView):
    """Edit an existing meetup"""
    template_name = "meetup/edit_meetup.html"
    model = Meetup
    slug_url_kwarg = "meetup_slug"
    form_class = EditMeetupForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_meetup", kwargs={"slug": self.object.meetup_location.slug,
                       "meetup_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(EditMeetupView, self).get_context_data(**kwargs)
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        context['meetup'] = self.meetup
        context['meetup_location'] = self.meetup.meetup_location
        return context


class UpcomingMeetupsView(MeetupLocationMixin, ListView):
    """List upcoming meetups of a meetup location"""
    template_name = "meetup/upcoming_meetups.html"
    model = Meetup
    paginate_by = 10

    def get_queryset(self, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        meetup_list = Meetup.objects.filter(
            meetup_location=self.meetup_location,
            date__gte=datetime.date.today()).order_by('date', 'time')
        return meetup_list

    def get_meetup_location(self):
        return self.meetup_location


class PastMeetupListView(MeetupLocationMixin, ListView):
    """List past meetups of a meetup location"""
    template_name = "meetup/past_meetups.html"
    model = Meetup
    paginate_by = 10

    def get_queryset(self, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        meetup_list = Meetup.objects.filter(
            meetup_location=self.meetup_location,
            date__lt=datetime.date.today()).order_by('date', 'time')
        return meetup_list

    def get_meetup_location(self):
        return self.meetup_location


class MeetupLocationSponsorsView(MeetupLocationMixin, DetailView):
    """View sponsors of a meetup location"""
    template_name = "meetup/sponsors.html"
    model = MeetupLocation

    def get_meetup_location(self):
        return get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])


class RemoveMeetupLocationMemberView(LoginRequiredMixin, MeetupLocationMixin, RedirectView):
    """Remove a member from a meetup location"""
    model = MeetupLocation
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)
        organizers = self.meetup_location.organizers.all()
        if systersuser in organizers and len(organizers) > 1:
            self.meetup_location.organizers.remove(systersuser)
        if systersuser not in self.meetup_location.organizers.all():
            self.meetup_location.members.remove(systersuser)
        return reverse('members_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get_meetup_location(self):
        return self.meetup_location


class AddMeetupLocationMemberView(LoginRequiredMixin, MeetupLocationMixin, UpdateView):
    """Add new member to meetup location"""
    template_name = "meetup/add_member.html"
    model = MeetupLocation
    form_class = AddMeetupLocationMemberForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful addition"""
        self.get_meetup_location()
        return reverse('members_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get_meetup_location(self):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        return self.meetup_location


class RemoveMeetupLocationOrganizerView(LoginRequiredMixin, MeetupLocationMixin, RedirectView):
    """Remove the 'organizer' status of a meetup location member"""
    model = MeetupLocation
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)
        organizers = self.meetup_location.organizers.all()
        if systersuser in organizers and len(organizers) > 1:
            self.meetup_location.organizers.remove(systersuser)
        return reverse('members_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get_meetup_location(self):
        return self.meetup_location


class MakeMeetupLocationOrganizerView(LoginRequiredMixin, MeetupLocationMixin, RedirectView):
    """Make a meetup location member an organizer of the location"""
    model = MeetupLocation
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)
        organizers = self.meetup_location.organizers.all()
        if systersuser not in organizers:
            self.meetup_location.organizers.add(systersuser)
        return reverse('members_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get_meetup_location(self):
        return self.meetup_location


class JoinMeetupLocationView(LoginRequiredMixin, MeetupLocationMixin, RedirectView):
    """Send a join request for a meetup location"""
    model = MeetupLocation
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        return reverse('about_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get(self, request, *args, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)

        join_requests = self.meetup_location.join_requests.all()
        members = self.meetup_location.members.all()

        if systersuser not in join_requests and systersuser not in members:
            self.meetup_location.join_requests.add(systersuser)
            msg = "Your request to join meetup location {0} has been sent. In a short while " \
                  "someone will review your request."
            messages.add_message(request, messages.SUCCESS, msg.format(self.meetup_location))
        elif systersuser in join_requests:
            msg = "You have already requested to join meetup location {0}. Please wait until " \
                  "someone reviews your request."
            messages.add_message(request, messages.WARNING, msg.format(self.meetup_location))
        elif systersuser in members:
            msg = "You are already a member of meetup location {0}."
            messages.add_message(request, messages.WARNING, msg.format(self.meetup_location))
        return super(JoinMeetupLocationView, self).get(request, *args, **kwargs)

    def get_meetup_location(self):
        return self.meetup_location


class MeetupLocationJoinRequestsView(LoginRequiredMixin, MeetupLocationMixin, DetailView):
    """View all join requests for a meetup location"""
    model = MeetupLocation
    template_name = "meetup/join_requests.html"
    paginated_by = 20

    def get_context_data(self, **kwargs):
        context = super(MeetupLocationJoinRequestsView, self).get_context_data(**kwargs)
        context['requests'] = self.object.join_requests.all()
        return context

    def get_meetup_location(self):
        return self.object


class ApproveMeetupLocationJoinRequestView(LoginRequiredMixin, MeetupLocationMixin, RedirectView):
    """Approve a join request for a meetup location"""
    model = MeetupLocation
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)
        self.meetup_location.members.add(systersuser)
        self.meetup_location.join_requests.remove(systersuser)
        return reverse('join_requests_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get_meetup_location(self):
        return self.meetup_location


class RejectMeetupLocationJoinRequestView(LoginRequiredMixin, MeetupLocationMixin, RedirectView):
    """Reject a join request for a meetup location"""
    model = MeetupLocation
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)
        self.meetup_location.join_requests.remove(systersuser)
        return reverse('join_requests_meetup_location', kwargs={'slug': self.meetup_location.slug})

    def get_meetup_location(self):
        return self.meetup_location


class AddMeetupLocationView(LoginRequiredMixin, MeetupLocationMixin, CreateView):
    """Add new meetup location"""
    template_name = "meetup/add_meetup_location.html"
    model = MeetupLocation
    form_class = AddMeetupLocationForm
    raise_exception = True

    def get_success_url(self):
        return reverse("about_meetup_location", kwargs={"slug": self.object.slug})

    def get_meetup_location(self):
        return self.object


class EditMeetupLocationView(LoginRequiredMixin, MeetupLocationMixin, UpdateView):
    """Edit an existing meetup location"""
    template_name = "meetup/edit_meetup_location.html"
    model = MeetupLocation
    form_class = EditMeetupLocationForm
    raise_exception = True

    def get_success_url(self):
        self.get_meetup_location()
        return reverse("about_meetup_location", kwargs={"slug": self.meetup_location.slug})

    def get_meetup_location(self, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        return self.meetup_location


class DeleteMeetupLocationView(LoginRequiredMixin, MeetupLocationMixin, DeleteView):
    """Delete an existing meetup location"""
    template_name = "meetup/meetup_location_confirm_delete.html"
    model = MeetupLocation
    raise_exception = True

    def get_success_url(self):
        return reverse("list_meetup_location")

    def get_meetup_location(self):
        return self.object

    def check_permissions(self, request):
        """Check if the request user has the permission to delete a meetup location.
        The permission holds true for superusers."""
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        return request.user.has_perm('delete_meetup_location', self.meetup_location)


class RsvpMeetupView(LoginRequiredMixin, MeetupLocationMixin, CreateView):
    """RSVP for a meetup"""
    template_name = "meetup/rsvp_meetup.html"
    model = Rsvp
    form_class = RsvpForm
    raise_exception = True

    def get_success_url(self):
        return reverse("view_meetup", kwargs={"slug": self.meetup_location.slug,
                                              "meetup_slug": self.object.meetup.slug})

    def get_form_kwargs(self):
        """Add request user and meetup object to the form kwargs.
        """
        kwargs = super(RsvpMeetupView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        kwargs.update({'meetup': self.meetup})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(RsvpMeetupView, self).get_context_data(**kwargs)
        context['meetup'] = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'],
                                              meetup_location=self.meetup_location)
        return context

    def get_meetup_location(self):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        return self.meetup_location


class RsvpGoingView(MeetupLocationMixin, ListView):
    """List of members whose rsvp status is 'coming'"""
    template_name = "meetup/rsvp_going.html"
    model = Rsvp
    paginated_by = 30

    def get_queryset(self, **kwargs):
        self.meetup_location = get_object_or_404(MeetupLocation, slug=self.kwargs['slug'])
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'],
                                        meetup_location=self.meetup_location)
        rsvp_list = Rsvp.objects.filter(meetup=self.meetup, coming=True)
        return rsvp_list

    def get_meetup_location(self):
        return self.meetup_location
