from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from common.mixins import UserDetailsMixin
from community.mixins import CommunityMenuMixin
from community.models import Community
from blog.forms import NewsForm
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


class CommunityNewsView(UserDetailsMixin, CommunityMenuMixin, DetailView):
    """Single Community view"""
    template_name = "blog/news.html"
    model = Community
    page_slug = 'news'

    def get_context_data(self, **kwargs):
        """Add Community object and News object to the context"""
        context = super(CommunityNewsView, self).get_context_data(**kwargs)
        context["community"] = self.object

        news_slug = self.kwargs['news_slug']
        context['news'] = get_object_or_404(News, slug=news_slug)
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class CreateCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                              CreateView):
    template_name = "blog/create_news.html"
    model = News
    form_class = NewsForm
    raise_exception = True
    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_news",
                       kwargs={"slug": self.community.slug,
                               "news_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and News object to the context"""
        context = super(CreateCommunityNewsView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        return context

    def get_form_kwargs(self):
        """Add request user and community object to the form kwargs.
        Used to autofill form fields with author and community without
        explicitly filling them up in the form."""
        kwargs = super(CreateCommunityNewsView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        kwargs.update({'community': self.community})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add new community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("add_community_news", self.community)
