import datetime
import operator

from django.contrib.gis.geoip2 import GeoIP2
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from braces.views import FormValidMessageMixin, FormInvalidMessageMixin
from geopy import Nominatim
from ipware import get_client_ip

from .forms import (AddMeetupForm, EditMeetupForm, AddMeetupCommentForm,
                    EditMeetupCommentForm, RsvpForm, AddSupportRequestForm,
                    EditSupportRequestForm, AddSupportRequestCommentForm,
                    EditSupportRequestCommentForm,
                    RequestMeetupForm, PastMeetup)
from .models import (Meetup, Rsvp, SupportRequest,
                     RequestMeetup, MeetupImages)
from .constants import (OK, SLUG_ALREADY_EXISTS, SLUG_ALREADY_EXISTS_MSG,
                        ERROR_MSG, SUCCESS_MEETUP_MSG)
from users.models import SystersUser
from common.models import Comment
from rest_framework.views import APIView
from cities_light.models import City


class RequestMeetupView(LoginRequiredMixin, CreateView):
    """View to Request a new meetup"""
    template_name = "meetup/request_new_meetup.html"
    model = RequestMeetup
    form_class = RequestMeetupForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        message = "Your request for a new meetup is successfully submitted. " \
                  "Please wait until someone reviews your request. "
        messages.add_message(self.request, messages.SUCCESS, message)
        return reverse('upcoming_meetups')

    def get_form_kwargs(self):
        """Add request user to the form kwargs.
        Used to autofill form fields with requestor without
        explicitly filling them up in the form."""
        kwargs = super(RequestMeetupView, self).get_form_kwargs()
        kwargs.update({'created_by': self.request.user})
        return kwargs


class NewMeetupRequestsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List of New Meetup Requests"""
    template_name = "meetup/new_meetup_requests.html"
    model = RequestMeetup
    raise_exception = True
    paginate_by = 10

    def get_queryset(self, **kwargs):
        """Set ListView queryset to all the unapproved meetup requests"""
        request_meetups_list = \
            RequestMeetup.objects.filter(is_approved=False).order_by('date', 'time')
        return request_meetups_list

    def check_permissions(self, request):
        """Check if the request user has the permission to view the meetup requests.
        The permission holds true for superusers."""
        return self.request.user.has_perm('meetup.view_meetup_request')


class ViewMeetupRequestView(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    """View the meetup request"""
    template_name = "meetup/view_new_meetup_request.html"
    form_class = RequestMeetupForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        """Add RequestMeetup object and it's verbose fields to the context."""
        context = super(ViewMeetupRequestView,
                        self).get_context_data(**kwargs)
        self.meetup_request = get_object_or_404(RequestMeetup, slug=self.kwargs['meetup_slug'])
        context['meetup_request'] = self.meetup_request
        context['meetup_request_fields'] = self.meetup_request.get_verbose_fields()
        return context

    def get_form_kwargs(self):
        """Add request user, meetup  to the form kwargs.
        Used to autofill form fields with requestor without
        explicitly filling them up in the form."""
        kwargs = super(ViewMeetupRequestView, self).get_form_kwargs()
        kwargs.update({'created_by': self.request.user})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permission to view meetup request .
        The permission holds true for superusers."""
        return self.request.user.has_perm("meetup.view_meetup_request")


class ApproveRequestMeetupView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    """Approve the new meetup request"""
    model = RequestMeetup
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        """Supply the redirect URL in case of successful approval.
        * Creates a new RequestMeetup object and copy fields,
            values from RequestMeetup object
        * Sets the RequestMeetup object's is_approved field to True.
        """
        meetup_request = get_object_or_404(RequestMeetup, slug=self.kwargs['meetup_slug'])
        new_meetup = Meetup()
        new_meetup.title = meetup_request.title
        new_meetup.slug = meetup_request.slug
        new_meetup.date = meetup_request.date
        new_meetup.time = meetup_request.time
        new_meetup.venue = meetup_request.venue
        new_meetup.description = meetup_request.description
        new_meetup.meetup_location = meetup_request.meetup_location
        new_meetup.leader = meetup_request.created_by
        meetup_request.is_approved = True
        meetup_request.approved_by = get_object_or_404(
            SystersUser, user=self.request.user)
        meetup_request.save()
        self.slug_meetup_request = meetup_request.slug
        status, message, level = self.process_request()
        messages.add_message(self.request, level, message)
        if status == OK:
            new_meetup.save()
            return reverse('view_meetup', kwargs={'slug': new_meetup.slug})
        else:
            return reverse('new_meetup_requests')

    def process_request(self):
        """If an error occurs during the creation of a new meetup, this method returns the
        status and message."""
        self.slug_meetup_values = Meetup.objects.all(
        ).values_list('slug', flat=True)
        if self.slug_meetup_request in self.slug_meetup_values:
            STATUS = SLUG_ALREADY_EXISTS
            return \
                STATUS, SLUG_ALREADY_EXISTS_MSG.format(self.slug_meetup_request), messages.WARNING
        else:
            STATUS = OK
        return STATUS, SUCCESS_MEETUP_MSG, messages.INFO

    def check_permissions(self, request):
        """Check if the request user has the permission to add a meetup .
        The permission holds true for superusers."""
        return self.request.user.has_perm("meetup.approve_meetup_request")


class RejectMeetupRequestView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Reject the new meetup request"""
    model = RequestMeetup
    template_name = "meetup/confirm_reject_request_meetup.html"
    raise_exception = True

    def get_success_url(self, *args, **kwargs):
        """Supply the success URL in case of a successful submit"""
        messages.add_message(self.request, messages.INFO,
                             "Meetup request successfullly rejected!")
        self.meetup_request = get_object_or_404(RequestMeetup, slug=self.kwargs['meetup_slug'])
        self.meetup_request.delete()
        return reverse('new_meetup_requests')

    def get_object(self, queryset=None):
        """Returns the RequestMeetup object"""
        self.meetup_request = get_object_or_404(RequestMeetup, slug=self.kwargs['meetup_slug'])
        return self.meetup_request

    def check_permissions(self, request):
        """Check if the request user has the permission to reject a meetup.
        The permission holds true for superusers."""
        return self.request.user.has_perm("meetup.reject_meetup_request")


class AllUpcomingMeetupsView(ListView):
    """List all upcoming meetups"""
    template_name = "meetup/list_meetup.html"
    model = Meetup

    def get_context_data(self, **kwargs):
        meetup_list = Meetup.objects.filter(
            date__gte=datetime.date.today()).order_by('date', 'time')
        context = super(AllUpcomingMeetupsView, self).get_context_data(**kwargs)
        context['cities_list'] = City.objects.all()
        context['meetup_list'] = meetup_list
        g = GeoIP2()
        client_ip, is_routable = get_client_ip(self.request)
        if is_routable:
            context['current_city'] = g.city(client_ip)['city']
        else:
            context['current_city'] = g.city("google.com")['city']
        return context


class MeetupView(DetailView):
    """View details of a meetup, including date, time, venue, description, number of users who
    rsvp'd and comments."""
    template_name = "meetup/meetup.html"
    model = Meetup

    def get_context_data(self, **kwargs):
        """Add Meetup object, number of users who rsvp'd and comments to the context"""
        context = super(MeetupView, self).get_context_data(**kwargs)
        context['meetup'] = self.object
        context['comments'] = Comment.objects.filter(
            content_type=ContentType.objects.get(app_label='meetup', model='meetup'),
            object_id=self.object.id,
            is_approved=True).order_by('date_created')
        coming_list = Rsvp.objects.filter(meetup=self.object, coming=True)
        plus_one_list = Rsvp.objects.filter(meetup=self.object, plus_one=True)
        context['coming_no'] = len(coming_list) + len(plus_one_list)
        context['share_message'] = self.object.title + " @systers_org "
        context['images'] = MeetupImages.objects.filter(meetup=self.object)
        return context


class AddMeetupView(FormValidMessageMixin, FormInvalidMessageMixin, LoginRequiredMixin,
                    PermissionRequiredMixin, CreateView):
    """Add new meetup"""
    template_name = "meetup/add_meetup.html"
    model = Meetup
    form_class = AddMeetupForm
    raise_exception = True
    form_valid_message = (u"Meetup added Successfully")
    form_invalid_message = ERROR_MSG

    def get_success_url(self):
        """Redirect to meetup view page in case of successful submit"""
        return reverse("view_meetup", kwargs={"slug": self.object.slug})

    def get_form_kwargs(self):
        """Add request user object to the form kwargs.
        Used to autofill form fields with created_by without
        explicitly filling them up in the form."""
        kwargs = super(AddMeetupView, self).get_form_kwargs()
        kwargs.update({'created_by': self.request.user,
                       'leader': self.request.user})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permission to add a meetup .
        The permission holds true for superusers."""
        return request.user.has_perm('meetup.add_meetups')


class DeleteMeetupView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete existing Meetup"""
    template_name = "meetup/meetup_confirm_delete.html"
    model = Meetup
    slug_url_kwarg = "meetup_slug"
    raise_exception = True

    def get_success_url(self):
        """Redirect to upcoming meetups page in case of successful deletion"""
        return reverse("upcoming_meetups")

    def check_permissions(self, request):
        """Check if the request user has the permission to delete a meetup.
         The permission holds true for superusers."""
        return request.user.has_perm('meetup.delete_meetups')


class EditMeetupView(FormValidMessageMixin, FormInvalidMessageMixin, LoginRequiredMixin,
                     PermissionRequiredMixin, UpdateView):
    """Edit an existing meetup"""
    template_name = "meetup/edit_meetup.html"
    model = Meetup
    slug_url_kwarg = "meetup_slug"
    form_class = EditMeetupForm
    form_valid_message = (u"Meetup edited Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to meetup view page in case of successful submit"""
        return reverse("view_meetup", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Meetup and MeetupLocation objects to the context"""
        context = super(EditMeetupView, self).get_context_data(**kwargs)
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        context['meetup'] = self.meetup
        context['meetup_location'] = self.meetup.meetup_location
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit a meetup.
        The permission holds true for superusers."""
        return request.user.has_perm('meetup.change_meetups')


class UpcomingMeetupsView(ListView):
    """List upcoming meetups of a meetup location"""
    template_name = "meetup/upcoming_meetups.html"
    model = Meetup
    paginate_by = 10

    def get_queryset(self, **kwargs):
        """Set ListView queryset to all the meetups whose date is equal to or greater than the
        current date"""
        meetup_list = \
            Meetup.objects.filter(date__gte=datetime.date.today()).order_by('date', 'time')
        return meetup_list


class PastMeetupListView(ListView):
    """List past meetups of a meetup location"""
    template_name = "meetup/past_meetups.html"
    model = Meetup
    paginate_by = 10

    def get_queryset(self, **kwargs):
        """Set ListView queryset to all the meetups whose date is less than the current date"""
        meetup_list = Meetup.objects.filter(date__lt=datetime.date.today()).order_by('date', 'time')
        return meetup_list


class AddMeetupCommentView(FormValidMessageMixin, FormInvalidMessageMixin, LoginRequiredMixin,
                           CreateView):
    """Add a comment to a Meetup"""
    template_name = "meetup/add_comment.html"
    model = Comment
    form_class = AddMeetupCommentForm
    form_valid_message = (u"Comment added Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the meetup view page in case of successful addition"""
        return reverse("view_meetup", kwargs={"slug": self.meetup.slug})

    def get_form_kwargs(self):
        """Add meetup object and request user to the form kwargs. Used to autofill form fields with
        content_object and author without explicitly filling them up in the form."""
        kwargs = super(AddMeetupCommentView, self).get_form_kwargs()
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        kwargs.update({'content_object': self.meetup})
        kwargs.update({'author': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(AddMeetupCommentView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        return context


class EditMeetupCommentView(FormValidMessageMixin, FormInvalidMessageMixin, LoginRequiredMixin,
                            PermissionRequiredMixin, UpdateView):
    """Edit a meetup's comment"""
    template_name = "meetup/edit_comment.html"
    model = Comment
    pk_url_kwarg = "comment_pk"
    form_class = EditMeetupCommentForm
    form_valid_message = (u"Comment edited Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the meetup view page in case of successful submission"""
        return reverse("view_meetup", kwargs={"slug": self.object.content_object.slug})

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(EditMeetupCommentView, self).get_context_data(**kwargs)
        context['meetup'] = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit a meetup comment."""
        self.comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        systersuser = get_object_or_404(SystersUser, user=request.user)
        return systersuser == self.comment.author


class DeleteMeetupCommentView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete a meetup's comment"""
    template_name = "meetup/comment_confirm_delete.html"
    model = Comment
    pk_url_kwarg = "comment_pk"
    raise_exception = True

    def get_success_url(self):
        """Redirect to the meetup view page in case of successful submission"""
        return reverse("view_meetup", kwargs={"slug": self.object.content_object.slug})

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(DeleteMeetupCommentView, self).get_context_data(**kwargs)
        context['meetup'] = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to delete a meetup comment."""
        self.comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        systersuser = get_object_or_404(SystersUser, user=request.user)
        return systersuser == self.comment.author


class RsvpMeetupView(FormValidMessageMixin, FormInvalidMessageMixin, LoginRequiredMixin,
                     CreateView):
    """RSVP for a meetup"""
    template_name = "meetup/rsvp_meetup.html"
    model = Rsvp
    form_class = RsvpForm
    form_valid_message = (u"Success")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the meetup view page in case of successful submission"""
        return reverse("view_meetup", kwargs={"slug": self.object.meetup.slug})

    def get_form_kwargs(self):
        """Add request user and meetup object to the form kwargs. Used to autofill form fields
        with user and meetup without explicitly filling them up in the form."""
        kwargs = super(RsvpMeetupView, self).get_form_kwargs()
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        kwargs.update({'user': self.request.user})
        kwargs.update({'meetup': self.meetup})
        currState = Rsvp.objects.filter(user__user=self.request.user, meetup=self.meetup)
        if currState.exists():
            kwargs.update({'instance': currState.first()})
        return kwargs

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(RsvpMeetupView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        return context


class RsvpGoingView(LoginRequiredMixin, ListView):
    """List of members whose rsvp status is 'coming'"""
    template_name = "meetup/rsvp_going.html"
    model = Rsvp
    paginated_by = 30

    def get_queryset(self, **kwargs):
        """Set ListView queryset to all rsvps whose 'coming' attribute is set to True"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        rsvp_list = Rsvp.objects.filter(meetup=self.meetup, coming=True)
        return rsvp_list

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(RsvpGoingView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        return context


class AddSupportRequestView(FormValidMessageMixin, FormInvalidMessageMixin,
                            LoginRequiredMixin, CreateView):
    """Add a Support Request for a meetup"""
    template_name = "meetup/add_support_request.html"
    model = SupportRequest
    form_class = AddSupportRequestForm
    form_valid_message = (u"Support Request submitted Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the support request view page in case of successful submission"""
        return reverse("view_support_request",
                       kwargs={"meetup_slug": self.meetup.slug, "pk": self.object.pk})

    def get_form_kwargs(self):
        """Add request user and meetup object to the form kwargs. Used to autofill form fields
        with volunteer and meetup without explicitly filling them up in the form."""
        kwargs = super(AddSupportRequestView, self).get_form_kwargs()
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        kwargs.update({'volunteer': self.request.user})
        kwargs.update({'meetup': self.meetup})
        return kwargs

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(AddSupportRequestView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        return context


class EditSupportRequestView(FormValidMessageMixin, FormInvalidMessageMixin,
                             LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edit an existing support request"""
    template_name = "meetup/edit_support_request.html"
    model = SupportRequest
    form_class = EditSupportRequestForm
    form_valid_message = (u"Support Request edited Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the support request view page in case of successful submission"""
        return reverse("view_support_request",
                       kwargs={"meetup_slug": self.object.meetup.slug, "pk": self.object.pk})

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(EditSupportRequestView, self).get_context_data(**kwargs)
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        context['meetup'] = self.meetup
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit a Support Request for a meetup.
        The permission holds true for superusers."""
        systersuser = get_object_or_404(SystersUser, user=request.user)
        self.suppportrequest = get_object_or_404(SupportRequest, pk=self.kwargs["pk"])
        return systersuser == self.suppportrequest.volunteer


class DeleteSupportRequestView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Delete existing Support Request"""
    template_name = "meetup/support_request_confirm_delete.html"
    model = SupportRequest
    raise_exception = True

    def get_success_url(self):
        """Redirect to the meetup view page in case of successful submission"""
        messages.success(self.request, 'Support Request Deleted.')
        return reverse("view_meetup", kwargs={"slug": self.object.meetup.slug})

    def check_permissions(self, request):
        """Check if the request user has the permission to delete a Support Request for a meetup.
        The permission holds true for superusers."""
        systersuser = get_object_or_404(SystersUser, user=request.user)
        self.suppportrequest = get_object_or_404(SupportRequest, pk=self.kwargs["pk"])
        return systersuser == self.suppportrequest.volunteer


class SupportRequestView(DetailView):
    """View a support request"""
    template_name = "meetup/support_request.html"
    model = SupportRequest

    def get_context_data(self, **kwargs):
        """Add Meetup object, SupportRequest object and approved comments to the context"""
        context = super(SupportRequestView, self).get_context_data(**kwargs)
        context['meetup'] = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        context['support_request'] = self.object
        context['comments'] = Comment.objects.filter(
            content_type=ContentType.objects.get(app_label='meetup', model='supportrequest'),
            object_id=self.object.id,
            is_approved=True).order_by('date_created')
        return context


class SupportRequestsListView(ListView):
    """List support requests for a meetup"""
    template_name = "meetup/list_support_requests.html"
    model = SupportRequest
    paginate_by = 10

    def get_queryset(self, **kwargs):
        """Set ListView queryset to all approved support requests of the meetup"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        supportrequest_list = SupportRequest.objects.filter(meetup=self.meetup, is_approved=True)
        return supportrequest_list

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(SupportRequestsListView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        return context


class UnapprovedSupportRequestsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """List unapproved support requests for a meetup"""
    template_name = "meetup/unapproved_support_requests.html"
    model = SupportRequest
    paginate_by = 10

    def get_queryset(self, **kwargs):
        """Set ListView queryset to all unapproved support requests of the meetup"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['slug'])
        supportrequest_list = SupportRequest.objects.filter(
            meetup=self.meetup, is_approved=False)
        return supportrequest_list

    def get_context_data(self, **kwargs):
        """Add Meetup object to the context"""
        context = super(UnapprovedSupportRequestsListView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to approve a support request."""
        return request.user.has_perm('meetup.approve_support_request')


class ApproveSupportRequestView(LoginRequiredMixin, PermissionRequiredMixin,
                                RedirectView):
    """Approve a support request for a meetup"""
    model = SupportRequest
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        """Approve the support request, send the user a notification and redirect to the unapproved
        support requests' page"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        support_request.is_approved = True
        support_request.save()
        return reverse('unapproved_support_requests', kwargs={'slug': self.meetup.slug})

    def check_permissions(self, request):
        """Check if the request user has the permission to approve a support request."""
        return request.user.has_perm('meetup.approve_support_request')


class RejectSupportRequestView(LoginRequiredMixin, PermissionRequiredMixin, RedirectView):
    """Reject a support request for a meetup"""
    model = SupportRequest
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        """Delete the support request and redirect to the unapproved support requests' page"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        support_request.delete()
        return reverse('unapproved_support_requests', kwargs={'slug': self.meetup.slug})

    def check_permissions(self, request):
        """Check if the request user has the permission to reject a support request."""
        return request.user.has_perm('meetup.reject_support_request')


class AddSupportRequestCommentView(FormValidMessageMixin, FormInvalidMessageMixin,
                                   LoginRequiredMixin, CreateView):
    """Add a comment to a Support Request"""
    template_name = "meetup/add_comment.html"
    model = Comment
    form_class = AddSupportRequestCommentForm
    form_valid_message = (u"Comment added Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the support request view page in case of successful submission"""
        return reverse('view_support_request',
                       kwargs={'meetup_slug': self.meetup.slug,
                               'pk': self.support_request.pk})

    def get_form_kwargs(self):
        """Add support request object and request user to the form kwargs. Used to autofill form
        fields with content_object and author without explicitly filling them up in the form."""
        kwargs = super(AddSupportRequestCommentView, self).get_form_kwargs()
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        self.support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        kwargs.update({'content_object': self.support_request})
        kwargs.update({'author': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        """Add Meetup and SupportRequest objects to the context"""
        context = super(AddSupportRequestCommentView, self).get_context_data(**kwargs)
        context['meetup'] = self.meetup
        context['support_request'] = self.support_request
        return context


class EditSupportRequestCommentView(FormValidMessageMixin, FormInvalidMessageMixin,
                                    LoginRequiredMixin, PermissionRequiredMixin,
                                    UpdateView):
    """Edit a support request's comment"""
    template_name = "meetup/edit_comment.html"
    model = Comment
    pk_url_kwarg = "comment_pk"
    form_class = EditSupportRequestCommentForm
    form_valid_message = (u"Comment edited Successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to the support request view page in case of successful submission"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        self.support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        return reverse("view_support_request", kwargs={"meetup_slug": self.meetup.slug,
                                                       "pk": self.support_request.pk})

    def get_context_data(self, **kwargs):
        """Add Meetup and SupportRequest objects to the context"""
        context = super(EditSupportRequestCommentView, self).get_context_data(**kwargs)
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        self.support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        context['meetup'] = self.meetup
        context['support_request'] = self.support_request
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit a comment to a Support Request"""
        self.comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        systersuser = get_object_or_404(SystersUser, user=request.user)
        return systersuser == self.comment.author


class DeleteSupportRequestCommentView(LoginRequiredMixin, PermissionRequiredMixin,
                                      DeleteView):
    """Delete a support request's comment"""
    template_name = "meetup/comment_confirm_delete.html"
    model = Comment
    pk_url_kwarg = "comment_pk"
    raise_exception = True

    def get_success_url(self):
        """Redirect to the support request view page in case of successful submission"""
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        self.support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        return reverse("view_support_request", kwargs={"meetup_slug": self.meetup.slug,
                                                       "pk": self.support_request.pk})

    def get_context_data(self, **kwargs):
        """Add Meetup and SupportRequest objects to the context"""
        context = super(DeleteSupportRequestCommentView, self).get_context_data(**kwargs)
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        self.support_request = get_object_or_404(SupportRequest, pk=self.kwargs['pk'])
        context['meetup'] = self.meetup
        context['support_request'] = self.support_request
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to edit a Support Request for a meetup"""
        self.comment = get_object_or_404(Comment, pk=self.kwargs['comment_pk'])
        systersuser = get_object_or_404(SystersUser, user=request.user)
        return systersuser == self.comment.author


class ApiForVmsView(APIView):

    @classmethod
    def return_meetup_data(self, meetups):
        """function to return all or filtered meetup data"""
        meetup_list = list()
        for meetup in meetups:
            meetup_data = {}
            meetup_data['meetup_id'] = meetup.pk
            meetup_data['event_name'] = meetup.title
            meetup_data['start_date'] = meetup.date
            meetup_data['venue'] = meetup.venue
            meetup_data['end_date'] = meetup.end_date
            meetup_data['description'] = meetup.description

            meetup_list.append(meetup_data)
        return JsonResponse(meetup_list, safe=False)

    @classmethod
    def get(self, request):
        # fetching all meetups
        meetups = Meetup.objects.all().order_by('date')
        apiforvmsview = ApiForVmsView()
        return (apiforvmsview.return_meetup_data(meetups))

    @classmethod
    def post(self, request):
        ID = request.data['meetup_id']
        # fetching all meetups whose id is greater than or equal to the date posted
        meetups = Meetup.objects.filter(pk__gte=ID).order_by('date')
        apiforvmsview = ApiForVmsView()
        return (apiforvmsview.return_meetup_data(meetups))


class UpcomingMeetupsSearchView(ListView):
    """Search Upcoming Meetups By  Keyword and Filter Date and Distance"""
    template_name = "meetup/list_meetup.html"
    model = Meetup

    @csrf_exempt
    def post(self, request):
        if request.method == 'POST':
            keyword = request.POST.get('keyword')
            location = request.POST.get('location')
            searched_meetups = Meetup.objects.filter(Q(date__gte=datetime.date.today()),
                                                     Q(title__icontains=keyword))
            results = list()
            unit = ''
            for meetup in searched_meetups:
                distance = ''
                geolocator = Nominatim(user_agent="Anita-B Portal", timeout=6)
                g = GeoIP2()
                if location == "Current Location":
                    client_ip, is_routable = get_client_ip(request)
                    if is_routable:
                        lat, long = g.lat_lon(client_ip)
                    else:
                        lat, long = g.lat_lon("google.com")
                    user_point = Point(float(long),
                                       float(lat))
                else:
                    user_loc = geolocator.geocode(location)
                    user_point = Point(float(user_loc.raw['lon']), float(user_loc.raw['lat']))
                meetup_loc = geolocator.geocode(meetup.meetup_location)
                meetup_point = Point(float(meetup_loc.raw['lon']),
                                     float(meetup_loc.raw['lat']))
                distance = int(user_point.distance(meetup_point)) * 100
                unit = 'kilometers from your location'

                results.append({'date': meetup.date,
                                'meetup': meetup.title,
                                'distance': distance,
                                'location': meetup.meetup_location.name,
                                'meetup_slug': meetup.slug})

            results.sort(key=operator.itemgetter('date'))
            results.sort(key=operator.itemgetter('distance'))
            return JsonResponse({'search_results': results, 'unit': unit}, safe=False)


class AddResourceView(FormValidMessageMixin, FormInvalidMessageMixin, LoginRequiredMixin,
                      PermissionRequiredMixin, UpdateView):
    """Add Resources and Images to a past meetup"""
    template_name = "meetup/edit_meetup.html"
    model = Meetup
    slug_url_kwarg = "meetup_slug"
    form_class = PastMeetup
    form_valid_message = (u"Resources added successfully")
    form_invalid_message = ERROR_MSG
    raise_exception = True

    def get_success_url(self):
        """Redirect to meetup view page in case of successful submit"""
        return reverse("view_meetup", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Meetup and MeetupLocation objects to the context"""
        context = super(AddResourceView, self).get_context_data(**kwargs)
        self.meetup = get_object_or_404(Meetup, slug=self.kwargs['meetup_slug'])
        context['meetup'] = self.meetup
        context['meetup_location'] = self.meetup.meetup_location
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to add resources to a meetup.
        The permission holds true for superusers."""
        return request.user.has_perm('meetup.add_resource')
