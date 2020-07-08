from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, ListView, FormView
from django.views.generic.detail import SingleObjectMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from community.models import Community
from membership.constants import *  # NOQA
from membership.forms import TransferOwnershipForm
from membership.models import JoinRequest
from users.models import SystersUser


class CommunityJoinRequestListView(LoginRequiredMixin, PermissionRequiredMixin,
                                   ListView):
    """List of not yet approved JoinRequest(s) to a Community"""
    template_name = "membership/join_requests.html"
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(CommunityJoinRequestListView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        return context

    def get_queryset(self):
        return JoinRequest.objects.filter(community=self.community,
                                          is_approved=False)

    def check_permissions(self, request):
        """Check if the request user has the permissions to approve join
        requests. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("approve_community_joinrequest",
                                     self.community)


class ApproveCommunityJoinRequestView(LoginRequiredMixin,
                                      PermissionRequiredMixin, RedirectView):
    """Approve a JoinRequest to a Community"""
    permanent = False
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to the list of join requests of the community"""
        return reverse("view_community_join_request_list",
                       kwargs={'slug': self.community.slug})

    def get(self, request, *args, **kwargs):
        """Add a message about the result of approving a join request"""
        message, level = self.process_join_request()
        messages.add_message(request, level, message)
        # TODO: notify the user about the acceptance
        return super(ApproveCommunityJoinRequestView, self).get(request, *args,
                                                                **kwargs)

    def process_join_request(self):
        """Approve the join request and make user member of the community.

        :return: tuple containing a string message and a message level
        """
        join_request = get_object_or_404(JoinRequest, community=self.community,
                                         pk=self.kwargs['pk'])
        user = join_request.user
        if user.is_member(self.community):
            join_request.delete()
            return USER_ALREADY_MEMBER_MSG.format(
                user, self.community), messages.INFO
        user.approve_all_join_requests(self.community)
        self.community.add_member(join_request.user)
        return USER_MEMBER_SUCCESS_MSG.format(
            user, self.community), messages.SUCCESS

    def check_permissions(self, request):
        """Check if the request user has the permissions to approve join
        requests. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("approve_community_joinrequest",
                                     self.community)


class RejectCommunityJoinRequestView(LoginRequiredMixin,
                                     PermissionRequiredMixin, RedirectView):
    """Reject a JoinRequest to a community"""
    permanent = False
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to the list of join requests of the community"""
        return reverse("view_community_join_request_list",
                       kwargs={'slug': self.community.slug})

    def get(self, request, *args, **kwargs):
        """Add a message about the result of rejecting a join request"""
        message, level = self.reject_join_request()
        messages.add_message(request, level, message)
        # TODO: notify the user about the rejection
        return super(RejectCommunityJoinRequestView, self).get(request, *args,
                                                               **kwargs)

    def reject_join_request(self):
        """Reject the user join request to a community.

        :return: tuple containing a string message and a message level
        """
        join_request = get_object_or_404(JoinRequest, community=self.community,
                                         pk=self.kwargs['pk'])
        user = join_request.user
        user.delete_all_join_requests(self.community)
        if user.is_member(self.community):
            return USER_ALREADY_MEMBER_MSG.format(
                user, self.community), messages.INFO
        return USER_MEMBER_REJECTED_MSG.format(
            user, self.community), messages.INFO

    def check_permissions(self, request):
        """Check if the request user has the permissions to approve/reject join
        requests. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("approve_community_joinrequest",
                                     self.community)


class RequestJoinCommunityView(LoginRequiredMixin, SingleObjectMixin,
                               RedirectView):
    """Request to join a community view"""
    model = Community
    permanent = False
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to the page the user was previously on"""
        return self.request.GET.get('current_url')

    def get(self, request, *args, **kwargs):
        """Attempt to create a join request and add a message about the result.
        """
        systers_user = get_object_or_404(SystersUser, user=self.request.user)
        community = self.get_object()
        join_request, status = JoinRequest.objects.create_join_request(
            systers_user, community)
        if status == OK:
            messages.add_message(request, messages.SUCCESS,
                                 JOIN_REQUEST_OK_MSG.format(community))
        elif status == ALREADY_MEMBER:
            messages.add_message(request, messages.WARNING,
                                 ALREADY_MEMBER_MSG.format(community))
        elif status == JOIN_REQUEST_EXISTS:
            messages.add_message(request, messages.WARNING,
                                 JOIN_REQUEST_EXISTS_MSG.format(community))
        else:
            pass
            # TODO: configure logging and log the unknown status
        return super(RequestJoinCommunityView, self).get(request, *args,
                                                         **kwargs)


class CancelCommunityJoinRequestView(LoginRequiredMixin, SingleObjectMixin,
                                     RedirectView):
    """Cancel a join request to a community view"""
    model = Community
    permanent = False
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to the page the user was previously on"""
        return self.request.GET.get('current_url')

    def get(self, request, *args, **kwargs):
        """Attempt to cancel user join request towards a community"""
        systers_user = get_object_or_404(SystersUser, user=self.request.user)
        community = self.get_object()
        status = JoinRequest.objects.cancel_join_request(systers_user,
                                                         community)
        if status == OK:
            messages.add_message(request, messages.SUCCESS,
                                 JOIN_REQUEST_CANCELED_MSG.format(community))
        elif status == ALREADY_MEMBER:
            messages.add_message(request, messages.WARNING,
                                 ALREADY_MEMBER_CANCEL_MSG.format(community))
        elif status == NO_PENDING_JOIN_REQUEST:
            messages.add_message(request, messages.WARNING,
                                 NO_PENDING_JOIN_REQUEST_MSG.format(community))
        else:
            pass
            # TODO: configure logging and log the unknown status
        return super(CancelCommunityJoinRequestView, self).get(request, *args,
                                                               **kwargs)


class LeaveCommunityView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    """Leave a community view"""
    model = Community
    permanent = False
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to user profile page"""
        return reverse("user", kwargs={'username': self.request.user.username})

    def get(self, request, *args, **kwargs):
        """Attempt to leave a community"""
        systers_user = get_object_or_404(SystersUser, user=self.request.user)
        community = self.get_object()
        status = systers_user.leave_community(community)
        if status == OK:
            messages.add_message(request, messages.SUCCESS,
                                 LEAVE_OK_MSG.format(community))
        elif status == NOT_MEMBER:
            messages.add_message(request, messages.WARNING,
                                 NOT_MEMBER_MSG.format(community))
        elif status == IS_ADMIN:
            messages.add_message(request, messages.WARNING,
                                 LEAVE_IS_ADMIN_MSG.format(community))
        else:
            pass
            # TODO: configure logging and log the unknown status
        return super(LeaveCommunityView, self).get(request, *args, **kwargs)


class TransferOwnershipView(LoginRequiredMixin, PermissionRequiredMixin,
                            FormView):
    """Transfer community ownership to another member."""
    template_name = "membership/transfer_ownership.html"
    form_class = TransferOwnershipForm
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Redirect to user profile"""
        return reverse("user", kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        """Add community object to the context"""
        context = super(TransferOwnershipView, self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def get_form_kwargs(self):
        """Add community object to form kwargs"""
        kwargs = super(TransferOwnershipView, self).get_form_kwargs()
        kwargs['community'] = self.community
        return kwargs

    def form_valid(self, form):
        """Since the form is valid, set the new admin of the community"""
        community = self.community
        new_admin_pk = form.cleaned_data['new_admin']
        new_admin = get_object_or_404(SystersUser, pk=int(new_admin_pk))
        status = community.set_new_admin(new_admin)
        if status == OK:
            messages.add_message(self.request, messages.SUCCESS,
                                 NEW_ADMIN_SUCCESS_MSG.format(community,
                                                              new_admin))
        else:
            pass
            # TODO: configure logging and log the unknown status
        return super(TransferOwnershipView, self).form_valid(form)

    def check_permissions(self, request):
        """Check if the request user is the community admin. Only the admin
        has the permission to transfer community ownership to another member
        of the community."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user == self.community.admin.user


class RemoveCommunityMemberView(LoginRequiredMixin, PermissionRequiredMixin,
                                RedirectView):
    """Remove a user from community members view"""
    permanent = False
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_redirect_url(self, *args, **kwargs):
        """Redirect to the management panel of community users"""
        return self.redirect_url

    def get(self, request, *args, **kwargs):
        """Process the removal of a user from community members and pass a
        status message to the user."""
        user = get_object_or_404(User, username=kwargs.get('username'))
        systersuser = get_object_or_404(SystersUser, user=user)
        status = systersuser.leave_community(self.community)
        self.redirect_url = reverse('community_users',
                                    kwargs={'slug': self.community.slug})
        if status == OK:
            if user == request.user:
                messages.add_message(request, messages.SUCCESS,
                                     LEAVE_OK_MSG.format(self.community))
                self.redirect_url = reverse('user',
                                            kwargs={'username': user.username})
            else:
                messages.add_message(request, messages.SUCCESS,
                                     REMOVE_OK_MSG.format(user,
                                                          self.community))
        elif status == NOT_MEMBER:
            messages.add_message(request, messages.WARNING,
                                 REMOVE_NOT_MEMBER_MSG.format(user,
                                                              self.community))
        elif status == IS_ADMIN:
            messages.add_message(request, messages.WARNING,
                                 REMOVE_IS_ADMIN_MSG.format(user,
                                                            self.community))
        else:
            pass
            # TODO: configure logging and log the unknown status
        return super(RemoveCommunityMemberView, self).get(request, *args,
                                                          **kwargs)

    def check_permissions(self, request):
        """Check if the request user has the permission to remove systers users
        from a community. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm('delete_community_systersuser',
                                     self.community)
