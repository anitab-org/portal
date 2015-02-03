from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, RedirectView, ListView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from community.forms import (CommunityForm, AddCommunityPageForm,
                             EditCommunityPageForm)
from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage, JoinRequest
from common.mixins import UserDetailsMixin


class CommunityLandingView(RedirectView):
    """View Community landing page, which might be a CommunityPage of lowest
    order or if pages are missing, then community news page."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """Provide a redirect url based on the following conditions:

        * if a Community has no pages, redirect to the news list views
        * if a Community has at least one page, redirect to the page with the
          lowest order (aka first page)
        """
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
    form_class = CommunityForm
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
                                            slug=self.kwargs['page_slug'])
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object

    def get_page_slug(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        page slug or the lack of it.

        :return: string CommunityPage slug
        """
        return self.kwargs['page_slug']


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


class CommunityJoinRequestListView(LoginRequiredMixin, PermissionRequiredMixin,
                                   ListView):
    """List of not yet approved JoinRequest(s) to a Community"""
    template_name = "community/join_requests.html"
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
        """Approve the join request and make user member of the community"""
        join_request = get_object_or_404(JoinRequest, community=self.community,
                                         pk=self.kwargs['pk'])
        user = join_request.user
        if user.is_member(self.community):
            join_request.delete()
            return "{0} is already a member of {1} community.".format(
                user, self.community), messages.INFO
        user.approve_all_join_requests(self.community)
        self.community.add_member(join_request.user)
        return "{0} successfully became a member of {1} community."\
            .format(user, self.community), messages.SUCCESS

    def check_permissions(self, request):
        """Check if the request user has the permissions to approve join
        requests. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("approve_community_joinrequest",
                                     self.community)
