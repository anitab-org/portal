from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.generic import DetailView, RedirectView, ListView, FormView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin, StaffuserRequiredMixin

from community.constants import (ORDER_NULL_MSG, ORDER_ALREADY_EXISTS_MSG,
                                 SLUG_ALREADY_EXISTS_MSG, ORDER_NULL,
                                 SLUG_ALREADY_EXISTS, ORDER_ALREADY_EXISTS, OK,
                                 SUCCESS_MSG)
from common.mixins import UserDetailsMixin
from community.forms import (EditCommunityForm, AddCommunityPageForm,
                             EditCommunityPageForm, PermissionGroupsForm,
                             RequestCommunityForm, EditCommunityRequestForm,
                             AddCommunityForm)
from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage, RequestCommunity
from users.models import SystersUser

from systers_portal.settings.base import GOOGLE_MAPS_API_KEY


class RequestCommunityView(LoginRequiredMixin, CreateView):
    """View to Request a new community"""
    template_name = "community/request_community.html"
    model = RequestCommunity
    form_class = RequestCommunityForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_request", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add the communities requested by the user to the context"""
        context = super(RequestCommunityView, self).get_context_data(**kwargs)
        self.systersuser = get_object_or_404(
            SystersUser, user=self.request.user)
        self.community_requests = RequestCommunity.objects.filter(
            user=self.systersuser)
        context['community_requests'] = self.community_requests
        return context

    def get_form_kwargs(self):
        """Add request user to the form kwargs.
        Used to autofill form fields with requestor without
        explicitly filling them up in the form."""
        kwargs = super(RequestCommunityView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class ViewCommunityRequestView(LoginRequiredMixin, PermissionRequiredMixin,
                               FormView):
    """View the community request"""
    template_name = "community/view_community_request.html"
    form_class = RequestCommunityForm
    raise_exception = True

    def get_context_data(self, **kwargs):
        """Add RequestCommunity object and it's verbose fields to the context."""
        context = super(ViewCommunityRequestView,
                        self).get_context_data(**kwargs)
        context['community_request'] = self.community_request
        context['community_request_fields'] = self.community_request.get_verbose_fields()
        return context

    def get_form_kwargs(self):
        """Add request user to the form kwargs.
        Used to autofill form fields with requestor without
        explicitly filling them up in the form."""
        kwargs = super(ViewCommunityRequestView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to view the community request.
        The permission holds true for superusers."""
        self.community_request = get_object_or_404(
            RequestCommunity, slug=self.kwargs['slug'])
        self.systersuser = get_object_or_404(
            SystersUser, user=self.request.user)
        return self.systersuser == self.community_request.user or request.user.is_superuser


class EditCommunityRequestView(LoginRequiredMixin, PermissionRequiredMixin,
                               UpdateView):
    """Edit the community request"""
    template_name = "community/edit_community_request.html"
    model = RequestCommunity
    form_class = EditCommunityRequestForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_request", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add RequestCommunity object to the context"""
        context = super(EditCommunityRequestView,
                        self).get_context_data(**kwargs)
        context['community_request'] = self.community_request
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to edit the community request.
        The permission holds true for superusers."""
        self.community_request = get_object_or_404(
            RequestCommunity, slug=self.kwargs['slug'])
        self.systersuser = get_object_or_404(
            SystersUser, user=self.request.user)
        return self.systersuser == self.community_request.user or request.user.is_superuser


class ApproveRequestCommunityView(LoginRequiredMixin, StaffuserRequiredMixin,
                                  RedirectView):
    """Approve the new community request"""
    model = RequestCommunity
    permanent = False
    raise_exception = True

    def get_redirect_url(self, *args, **kwargs):
        """Supply the redirect URL in case of successful approval.
        * Creates a new Community object and copy fields, values from RequestCommunity object
        * Sets the requestor as the community admin
        * Sets the RequestCommunity object's is_approved field to True.
        """
        community_request = get_object_or_404(
            RequestCommunity, slug=self.kwargs['slug'])
        new_community = Community()
        community_request_fields = community_request.get_fields()
        self.order_community_request = community_request.order
        self.slug_communtiy_request = community_request.slug
        new_community_fields = [
            field.name for field in new_community._meta.fields]
        fields = [(field_name, field_value) for field_name, field_value in community_request_fields
                  if field_name in new_community_fields]
        for field_name, field_value in fields:
            setattr(new_community, field_name, field_value)

        self.systersuser = community_request.user
        new_community.admin = self.systersuser
        self.admin = get_object_or_404(SystersUser, user=self.request.user)
        status, message, level = self.process_request()
        if status == OK:
            new_community.save()
            community_request.is_approved = True
            community_request.approved_by = self.admin
            community_request.save()
            messages.add_message(self.request, level, message)
            return reverse("view_community_landing", kwargs={"slug": new_community.slug})
        else:
            messages.add_message(self.request, level, message)
            return reverse("edit_community_request", kwargs={"slug": community_request.slug})

    def process_request(self):
        """If an error occurs during the creation of a new community, this method returns the
        status and message."""
        self.order_community_values = list(
            Community.objects.all().values_list('order', flat=True))
        self.order_community_values.sort()
        self.slug_community_values = Community.objects.all().values_list('slug', flat=True)
        if self.order_community_request is None:
            STATUS = ORDER_NULL
            return STATUS, ORDER_NULL_MSG, messages.INFO
        elif self.order_community_request in self.order_community_values:
            STATUS = ORDER_ALREADY_EXISTS
            string_order_values = ', '.join(
                map(str, self.order_community_values))
            return STATUS, ORDER_ALREADY_EXISTS_MSG.format(self.order_community_request,
                                                           string_order_values), messages.INFO
        elif self.slug_communtiy_request in self.slug_community_values:
            STATUS = SLUG_ALREADY_EXISTS
            string_slug_values = ', '.join(
                map(str, self.slug_community_values))
            return STATUS, SLUG_ALREADY_EXISTS_MSG.format(self.slug_communtiy_request,
                                                          string_slug_values), messages.INFO
        else:
            STATUS = OK
            return STATUS, SUCCESS_MSG, messages.INFO


class RejectRequestCommunityView(LoginRequiredMixin, StaffuserRequiredMixin, DeleteView):
    """Reject the new Community Request"""
    model = RequestCommunity
    template_name = "community/confirm_reject_request_community.html"
    raise_exception = True

    def get_success_url(self):
        """Supply the success URL in case of successful submit"""
        messages.add_message(self.request, messages.INFO,
                             "Community request successfullly rejected!")
        community_request = get_object_or_404(
            RequestCommunity, slug=self.kwargs['slug'])
        community_request.delete()
        return reverse('unapproved_community_requests')


class NewCommunityRequestsListView(LoginRequiredMixin, StaffuserRequiredMixin, ListView):
    """List of Community Requests"""
    template_name = "community/new_community_requests.html"
    model = RequestCommunity
    raise_exception = True
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """Add RequestCommunity object to the context"""
        context = super(NewCommunityRequestsListView,
                        self).get_context_data(**kwargs)
        self.systersuser = get_object_or_404(
            SystersUser, user=self.request.user)
        context['requestor'] = self.systersuser
        return context

    def get_queryset(self):
        """Set ListView queryset to all the unapproved community requests"""
        request_community_list = RequestCommunity.objects.filter(
            is_approved=False)
        return request_community_list


class CommunityLandingView(RedirectView):
    """View Community landing page, which might be a CommunityPage of lowest
    order or if pages are missing, then community news page."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """Provide a redirect url based on the following conditions:
        * if a Community has no pages, redirect to the news list views
        * if a Community has at least one page, redirect to the page with the
          lowest order (aka first page)"""
        community = get_object_or_404(Community, slug=kwargs['slug'])
        community_pages = CommunityPage.objects.filter(
            community=community).order_by('order')
        if community_pages.exists():
            community_page_slug = community_pages[0].slug
            return reverse("view_community_page",
                           kwargs={"slug": community.slug,
                                   "page_slug": community_page_slug})
        else:
            return reverse("view_community_news_list",
                           kwargs={'slug': community.slug})


class ViewCommunityProfileView(DetailView):
    """Community profile view"""
    template_name = "community/view_profile.html"
    model = Community


class EditCommunityProfileView(LoginRequiredMixin, PermissionRequiredMixin,
                               UpdateView):
    """Edit community profile view"""
    template_name = "community/edit_profile.html"
    model = Community
    form_class = EditCommunityForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse('view_community_profile',
                       kwargs={'slug': self.object.slug})

    def check_permissions(self, request):
        """Check if the request user has the permissions to change community
        profile. The permission holds true for superusers."""
        community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("change_community", community)


class CommunityPageView(UserDetailsMixin, CommunityMenuMixin, DetailView):
    """Community page view"""
    template_name = "community/page.html"
    model = Community

    def get_context_data(self, **kwargs):
        """Add to the context CommunityPage object"""
        context = super(CommunityPageView, self).get_context_data(**kwargs)
        context['page'] = get_object_or_404(CommunityPage,
                                            community=self.object,
                                            slug=self.kwargs['page_slug'])
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.
        :return: Community object"""
        return self.object

    def get_page_slug(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        page slug or the lack of it.
        :return: string CommunityPage slug"""
        return self.kwargs['page_slug']


class AddCommunityView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = "community/add_community.html"
    model = Community
    form_class = AddCommunityForm
    raise_exception = True

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_landing",
                       kwargs={"slug": self.object.slug})

    def get_form_kwargs(self):
        """Add admin to the form kwargs.
        Used to autofill form fields with admin without
        explicitly filling them up in the form."""
        kwargs = super(AddCommunityView, self).get_form_kwargs()
        kwargs.update({'admin': self.systersuser})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add a new community.
        The permission holds true for superusers."""
        self.systersuser = get_object_or_404(SystersUser, user=request.user)
        return request.user.has_perm("add_community")


class AddCommunityPageView(LoginRequiredMixin, PermissionRequiredMixin,
                           CreateView):
    """Add new Community page view"""
    template_name = "common/add_post.html"
    model = CommunityPage
    form_class = AddCommunityPageForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_page",
                       kwargs={"slug": self.community.slug,
                               "page_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(AddCommunityPageView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'page'
        return context

    def get_form_kwargs(self):
        """Add request user and community object to the form kwargs.
        Used to autofill form fields with author and community without
        explicitly filling them up in the form."""
        kwargs = super(AddCommunityPageView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        kwargs.update({'community': self.community})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add new community
        page. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("add_community_page", self.community)


class EditCommunityPageView(LoginRequiredMixin, PermissionRequiredMixin,
                            UpdateView):
    """Edit an existing Community page view"""
    template_name = "common/edit_post.html"
    model = CommunityPage
    slug_url_kwarg = "page_slug"
    form_class = EditCommunityPageForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_page",
                       kwargs={"slug": self.community.slug,
                               "page_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(EditCommunityPageView, self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to edit community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("change_community_page",
                                     self.community)


class DeleteCommunityPageView(LoginRequiredMixin, PermissionRequiredMixin,
                              DeleteView):
    """Delete existing Community page view"""
    template_name = "common/post_confirm_delete.html"
    model = CommunityPage
    slug_url_kwarg = "page_slug"
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful deletion"""
        return reverse("view_community_landing",
                       kwargs={"slug": self.community.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(DeleteCommunityPageView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'page'
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to delete community
        page. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("delete_community_page", self.community)


class CommunityUsersView(LoginRequiredMixin, PermissionRequiredMixin,
                         ListView):
    """Manage Community users view"""
    template_name = "community/users.html"
    paginate_by = 50
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_queryset(self):
        """Set ListView queryset to all the members of the community"""
        return self.community.members.all()

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(CommunityUsersView, self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def check_permissions(self, request):
        """Check if the request user has the permission to manage community
        users (add, change, delete). The permission holds true for
        superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        add_perm = request.user.has_perm("add_community_systersuser",
                                         self.community)
        change_perm = request.user.has_perm("change_community_systersuser",
                                            self.community)
        delete_perm = request.user.has_perm("delete_community_systersuser",
                                            self.community)
        return add_perm and change_perm and delete_perm


class UserPermissionGroupsView(LoginRequiredMixin, PermissionRequiredMixin,
                               FormView):
    """Manage user permission groups"""
    template_name = "community/permissions.html"
    form_class = PermissionGroupsForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """On success redirect to the manage community users page"""
        return reverse("community_users", kwargs={'slug': self.community.slug})

    def get_form_kwargs(self):
        """Add community object to form kwargs"""
        kwargs = super(UserPermissionGroupsView, self).get_form_kwargs()
        kwargs['community'] = self.community
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        self.systersuser = SystersUser.objects.get(user=user)
        kwargs['user'] = self.systersuser
        return kwargs

    def get_context_data(self, **kwargs):
        """Add Community object and SystersUser objects to the context"""
        context = super(UserPermissionGroupsView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['systersuser'] = self.systersuser
        return context

    def form_valid(self, form):
        """If the form is valid, call save method on it."""
        if form.has_changed():
            form.save()
        return super(UserPermissionGroupsView, self).form_valid(form)

    def check_permissions(self, request):
        """Check if the request user has the permission to change user
        permission groups. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("change_community_systersuser",
                                     self.community)


class CommunitySearch(ListView):
    """Search for Communities View"""
    template_name = "community/community_search.html"
    model = Community

    def get(self, request):
        if request.method == 'GET':
            context = {}
            url_parameter = request.GET.get("query")
            if url_parameter:
                communities = Community.objects.filter(name__icontains=url_parameter)
            else:
                communities = Community.objects.all()
            context['communities'] = communities
            context['api_key'] = GOOGLE_MAPS_API_KEY
            if request.is_ajax():
                html = render_to_string(
                    template_name="community/snippets/search-snippet.html",
                    context={"communities": communities}
                )
                data_dict = {"html": html}
                return JsonResponse(data=data_dict)
            return render(request, "community/community_search.html", context=context)
