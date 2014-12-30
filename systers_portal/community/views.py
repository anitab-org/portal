from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from community.forms import CommunityForm
from community.mixins import CommunityMenuMixin
from community.models import Community, CommunityPage
from blog.models import News
from users.models import SystersUser


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


class CommunityPageView(CommunityMenuMixin, DetailView):
    """Community page view"""
    template_name = "community/base.html"
    model = Community

    def get_context_data(self, **kwargs):
        """Supply additional context data, such as:

        * SystersUser object
        * Indicator if user is member of the community
        * JoinRequest object if exists
        """
        context = super(CommunityPageView, self).get_context_data(**kwargs)
        community = context['community']
        user = self.request.user
        if user.username:
            systers_user = SystersUser.objects.get(user=user)
            context['is_member'] = systers_user.is_member(community)
            context['join_request'] = systers_user.get_last_join_request(
                community)
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        community_slug = self.kwargs['slug']
        return get_object_or_404(Community, slug=community_slug)

    def get_page(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        page or the lack of it.

        :return: CommunityPage object if provided, otherwise None
        """
        page_slug = self.kwargs.get('page_slug')
        if page_slug:
            return get_object_or_404(CommunityPage, slug=page_slug)
        return None

        return context
