from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin

from users.models import SystersUser


class UserProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = "users/view_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        username = context['username']
        systersuser = get_object_or_404(SystersUser, user__username=username)
        context['systersuser'] = systersuser
        return context
