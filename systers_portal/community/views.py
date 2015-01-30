from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.detail import SingleObjectMixin

from community.forms import CommunityForm
from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage
from common.mixins import UserDetailsMixin


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


class CommunityPageListView(UserDetailsMixin, CommunityMenuMixin,
                            SingleObjectMixin, ListView):
    template_name = "community/page_list.html"
    # TODO: add pagination

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Community.objects.all())
        return super(CommunityPageListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CommunityPageListView, self).get_context_data(**kwargs)
        context["community"] = self.object
        context["news_list"] = self.object_list
        return context

    def get_queryset(self):
        return CommunityPage.objects.filter(community=self.object)

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class CommunityPageView(UserDetailsMixin, CommunityMenuMixin, DetailView):
    """Community page view"""
    template_name = "community/page.html"
    model = Community

    def get_context_data(self, **kwargs):
        """Add Community object and News object to the context"""
        context = super(CommunityPageView, self).get_context_data(**kwargs)
        context["community"] = self.object

        slug = self.kwargs.get('page_slug')
        context['page'] = get_object_or_404(CommunityPage, slug=slug)
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
        return self.kwargs.get('page_slug')
