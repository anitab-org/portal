from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, RedirectView, ListView, FormView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from common.mixins import UserDetailsMixin
from community.forms import (CommunityForm, AddCommunityPageForm,
                             EditCommunityPageForm, PermissionGroupsForm)
from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage
from users.models import SystersUser


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
                                            community=self.object,
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
