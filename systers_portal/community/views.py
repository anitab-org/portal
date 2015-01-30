from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, RedirectView
from django.views.generic.edit import UpdateView, CreateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from community.forms import (CommunityForm, AddCommunityPageForm,
                             EditCommunityPageForm)
from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage
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
