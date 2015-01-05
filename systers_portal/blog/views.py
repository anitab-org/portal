from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from common.mixins import UserDetailsMixin
from community.mixins import CommunityMenuMixin
from community.models import Community
from blog.models import News


class CommunityNewsListView(UserDetailsMixin, CommunityMenuMixin,
                            SingleObjectMixin, ListView):
    """List of Community news view"""
    template_name = "blog/news_list.html"
    page_slug = 'news'
    # TODO: add pagination

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Community.objects.all())
        return super(CommunityNewsListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add Community object and News list to the context under different
        names."""
        context = super(CommunityNewsListView, self).get_context_data(**kwargs)
        context["community"] = self.object
        context["news_list"] = self.object_list
        return context

    def get_queryset(self):
        return News.objects.filter(community=self.object)

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object
