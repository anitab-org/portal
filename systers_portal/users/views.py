from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from braces.views import LoginRequiredMixin, MultiplePermissionsRequiredMixin

from membership.models import JoinRequest
from users.forms import UserForm, EditUserSettings
from users.models import SystersUser, UserSetting


class UserView(LoginRequiredMixin, TemplateView):
    """User view"""
    template_name = "users/view_profile.html"

    def get_context_data(self, **kwargs):
        """Supply additional context data for the template, such as:

        * SystersUser object
        * Community objects SystersUser is member of
        * SystersUser JoinRequest objects not (yet) approved
        * Group objects SystersUser is member of
        """
        context = super(UserView, self).get_context_data(**kwargs)
        username = context['username']
        systersuser = get_object_or_404(SystersUser, user__username=username)
        communities = systersuser.communities.all()
        join_requests = JoinRequest.objects.filter(user=systersuser,
                                                   is_approved=False)
        permission_groups = systersuser.user.groups.all()
        context_dict = {'systersuser': systersuser,
                        'community_list': communities,
                        'join_requests': join_requests,
                        'permission_groups': permission_groups}
        for key, value in context_dict.items():
            context[key] = value
        return context


class UserProfileView(LoginRequiredMixin, MultiplePermissionsRequiredMixin,
                      UpdateView):
    """User profile update view"""
    template_name = "users/edit_profile.html"
    form_class = UserForm
    model = User
    raise_exception = True

    # TODO: add `redirect_unauthenticated_users = True` when django-braces will
    # reach version 1.5

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch method to add to the view User and SystersUser
        objects, of which the profile is displayed."""
        username = kwargs.get('username')
        self.user = get_object_or_404(User, username=username)
        self.systersuser = get_object_or_404(SystersUser, user=self.user)
        return super(UserProfileView, self).dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        """Get form instance"""
        return self.user

    def get_context_data(self, **kwargs):
        """Supply additional context data for the template"""
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['systersuser'] = self.systersuser
        return context

    def get_success_url(self):
        """Supply the redirect URL in case of successful submit"""
        return self.systersuser.get_absolute_url()

    def check_permissions(self, request):
        """Check if the request user has any of those permissions:

        * is a superuser
        * is the owner of the profile (can edit it's own profile)
        * has the permission to change a community systersuser, if systersuser
          is member of any of those communities
        """
        permissions = []
        communities = self.systersuser.communities.all()
        for community in communities:
            permissions.extend([
                request.user.has_perm("change_community_systersuser",
                                      community)])
        permissions.extend([request.user.is_superuser])
        permissions.extend([request.user == self.user])
        return any(permissions)


class EditSettings(UpdateView, LoginRequiredMixin):
    model = UserSetting
    template_name = "users/settings.html"
    form_class = EditUserSettings
    raise_exception = True
    form_valid_message = u"Settings updated Successfully"

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.request.user.username})

    def get_form_kwargs(self):
        kwargs = super(EditSettings, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self):
        systersuser = SystersUser.objects.get(user=self.request.user)
        return UserSetting.objects.get(user=systersuser)
