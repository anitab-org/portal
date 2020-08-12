from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView, UpdateView,
                                  DeleteView, TemplateView)
from django.views.generic.detail import SingleObjectMixin
from braces.views import LoginRequiredMixin, PermissionRequiredMixin

from common.mixins import UserDetailsMixin
from community.mixins import CommunityMenuMixin
from community.models import Community
from blog.forms import (AddNewsForm, EditNewsForm, AddResourceForm,
                        EditResourceForm, TagForm, ResourceTypeForm)
from blog.mixins import ResourceTypesMixin
from blog.models import News, Resource, ResourceType, Tag

from users.models import SystersUser

from blog.models import UserPins


class CommunityNewsListView(UserDetailsMixin, CommunityMenuMixin,
                            SingleObjectMixin, ListView):
    """List of Community news view"""
    template_name = "blog/post_list.html"
    page_slug = 'news'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Community.objects.all())
        return super(CommunityNewsListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add Community object under different name and type of post."""
        context = super(CommunityNewsListView, self).get_context_data(**kwargs)
        context["community"] = self.object
        context["post_type"] = "news"
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
    """Single News Community view"""
    template_name = "blog/post.html"
    model = Community
    page_slug = 'news'

    def get_context_data(self, **kwargs):
        """Add Community object, News object and post type to the context"""
        context = super(CommunityNewsView, self).get_context_data(**kwargs)
        context["community"] = self.object

        news_slug = self.kwargs['news_slug']
        context['post'] = get_object_or_404(News, community=self.object,
                                            slug=news_slug)
        context["post_type"] = "news"
        context["share_message"] = self.object.name + " @systers_org " + context['post'].title
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class AddCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                           CreateView):
    """Add News to a Community view"""
    template_name = "common/add_post.html"
    model = News
    form_class = AddNewsForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_news",
                       kwargs={"slug": self.community.slug,
                               "news_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(AddCommunityNewsView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'news'
        return context

    def get_form_kwargs(self):
        """Add request user and community object to the form kwargs.
        Used to autofill form fields with author and community without
        explicitly filling them up in the form."""
        kwargs = super(AddCommunityNewsView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        kwargs.update({'community': self.community})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add new community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("add_community_news", self.community)


class EditCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                            UpdateView):
    """Edit existing Community News view"""
    template_name = "common/edit_post.html"
    model = News
    slug_url_kwarg = "news_slug"
    form_class = EditNewsForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_news",
                       kwargs={"slug": self.community.slug,
                               "news_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(EditCommunityNewsView, self).get_context_data(**kwargs)
        context['community'] = self.community
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to edit community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("change_community_news", self.community)


class DeleteCommunityNewsView(LoginRequiredMixin, PermissionRequiredMixin,
                              DeleteView):
    """Delete existing Community News view"""
    template_name = "common/post_confirm_delete.html"
    model = News
    slug_url_kwarg = "news_slug"
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful deletion"""
        return reverse("view_community_news_list",
                       kwargs={"slug": self.community.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(DeleteCommunityNewsView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'news'
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to delete community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("delete_community_news", self.community)


class CommunityResourceListView(UserDetailsMixin, CommunityMenuMixin,
                                ResourceTypesMixin, SingleObjectMixin,
                                ListView):
    """List of Community resources view"""
    template_name = "blog/post_list.html"
    page_slug = 'resources'
    paginate_by = 5

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Community.objects.all())
        return super(CommunityResourceListView, self).get(request, *args,
                                                          **kwargs)

    def get_context_data(self, **kwargs):
        """Add Community object under different name and type of post."""
        context = super(CommunityResourceListView, self).get_context_data(
            **kwargs)
        context["community"] = self.object
        context["post_type"] = "resource"
        return context

    def get_queryset(self):
        """Get the list of Resource objects filtered or not by their resource
        type"""
        type_query = self.request.GET.get("type", "")
        if type_query:
            resource_type = ResourceType.objects.filter(name=type_query)
            if resource_type:
                return Resource.objects.filter(community=self.object,
                                               resource_type=resource_type[0])
        return Resource.objects.filter(community=self.object)

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class CommunityResourceView(UserDetailsMixin, CommunityMenuMixin, DetailView):
    """Resource Community view"""
    template_name = "blog/post.html"
    model = Community
    page_slug = 'resources'

    def get_context_data(self, **kwargs):
        """Add Community object, Resource object and post type to the
        context"""
        context = super(CommunityResourceView, self).get_context_data(**kwargs)
        context["community"] = self.object
        resource_slug = self.kwargs['resource_slug']
        if self.request.user.is_authenticated:
            user = SystersUser.objects.get(user=self.request.user)
            user_pins = UserPins.objects.filter(user=user)
            if user_pins:
                context['pins'] = user_pins.first().pins.all()
            else:
                context['pins'] = []
        else:
            context['pins'] = []
        context["post"] = get_object_or_404(Resource, community=self.object,
                                            slug=resource_slug)
        context["post_type"] = "resource"
        return context

    def get_community(self):
        """Overrides the method from CommunityMenuMixin to extract the current
        community.

        :return: Community object
        """
        return self.object


class AddCommunityResourceView(LoginRequiredMixin, PermissionRequiredMixin,
                               CreateView):
    """Add News to a Community view"""
    template_name = "common/add_post.html"
    model = Resource
    form_class = AddResourceForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_resource",
                       kwargs={"slug": self.community.slug,
                               "resource_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(AddCommunityResourceView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'resource'
        return context

    def get_form_kwargs(self):
        """Add request user and community object to the form kwargs.
        Used to autofill form fields with author and community without
        explicitly filling them up in the form."""
        kwargs = super(AddCommunityResourceView, self).get_form_kwargs()
        kwargs.update({'author': self.request.user})
        kwargs.update({'community': self.community})
        return kwargs

    def check_permissions(self, request):
        """Check if the request user has the permissions to add new community
        resource. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("add_community_resource", self.community)


class EditCommunityResourcesView(LoginRequiredMixin, PermissionRequiredMixin,
                                 UpdateView):
    """Edit existing Community Resource view"""
    template_name = "common/edit_post.html"
    model = Resource
    slug_url_kwarg = "resource_slug"
    form_class = EditResourceForm
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return reverse("view_community_resource",
                       kwargs={"slug": self.community.slug,
                               "resource_slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(EditCommunityResourcesView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to edit community
        news. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("change_community_resource",
                                     self.community)


class DeleteCommunityResourceView(LoginRequiredMixin, PermissionRequiredMixin,
                                  DeleteView):
    """Delete existing Community Resource view"""
    template_name = "common/post_confirm_delete.html"
    model = Resource
    slug_url_kwarg = "resource_slug"
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Supply the redirect URL in case of successful deletion"""
        return reverse("view_community_resource_list",
                       kwargs={"slug": self.community.slug})

    def get_context_data(self, **kwargs):
        """Add Community object and post type to the context"""
        context = super(DeleteCommunityResourceView, self).get_context_data(
            **kwargs)
        context['community'] = self.community
        context['post_type'] = 'resource'
        return context

    def check_permissions(self, request):
        """Check if the request user has the permissions to delete community
        resource. The permission holds true for superusers."""
        self.community = get_object_or_404(Community, slug=self.kwargs['slug'])
        return request.user.has_perm("delete_community_resource",
                                     self.community)


class AddTagView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create a new Tag"""
    template_name = "blog/tag_type.html"
    model = Tag
    form_class = TagForm
    permission_required = "blog.add_tag"
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Redirect to previous page"""
        return reverse("view_community_news_list",
                       kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(AddTagView, self).get_context_data(**kwargs)
        context['community'] = get_object_or_404(Community,
                                                 slug=self.kwargs['slug'])
        context['tag_type'] = "tag"
        return context


class AddResourceTypeView(LoginRequiredMixin, PermissionRequiredMixin,
                          CreateView):
    """Create a new Resource Type"""
    template_name = "blog/tag_type.html"
    model = ResourceType
    form_class = ResourceTypeForm
    permission_required = "blog.add_resourcetype"
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def get_success_url(self):
        """Redirect to previous page"""
        return reverse("view_community_resource_list",
                       kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        """Add Community object to the context"""
        context = super(AddResourceTypeView, self).get_context_data(**kwargs)
        context['community'] = get_object_or_404(Community,
                                                 slug=self.kwargs['slug'])
        context['tag_type'] = "Resource Type"
        return context


class UserPinView(LoginRequiredMixin, ListView):
    template_name = "blog/post.html"
    model = Resource

    def post(self, request, resource_slug, slug):
        if request.method == "POST":
            community = get_object_or_404(Community, slug=slug)
            resource = get_object_or_404(Resource, community=community,
                                         slug=resource_slug)
            user = SystersUser.objects.get(user=self.request.user)
            user_pins = UserPins.objects.filter(user=user)
            if user_pins:
                user_pins.first().add_pin(resource)
            else:
                user_pins = UserPins.objects.create(user=user)
                user_pins.add_pin(resource)
            return JsonResponse({}, safe=False, status=200)


class RemovePinView(LoginRequiredMixin, ListView):
    template_name = "blog/post.html"
    model = Resource

    def post(self, request, resource_slug, slug):
        if request.method == "POST":
            status_code = 200
            community = get_object_or_404(Community, slug=slug)
            resource = get_object_or_404(Resource, community=community,
                                         slug=resource_slug)
            user = SystersUser.objects.get(user=self.request.user)
            user_pins = UserPins.objects.filter(user=user)
            if resource in user_pins.first().pins.all():
                user_pins.first().remove_pin(resource)
            else:
                status_code = 404
            return JsonResponse({}, safe=False, status=status_code)


class RemovePinFromListView(LoginRequiredMixin, TemplateView):
    template_name = "users/pins.html"

    def post(self, request, username):
        if request.method == "POST":
            status_code = 200
            user = SystersUser.objects.get(user=self.request.user)
            user_pins = UserPins.objects.filter(user=user)
            resource = get_object_or_404(Resource, id=request.POST.get('id'))
            if resource in user_pins.first().pins.all():
                user_pins.first().remove_pin(resource)
            else:
                status_code = 404
            return JsonResponse({}, safe=False, status=status_code)
