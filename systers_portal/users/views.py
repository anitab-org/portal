from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin

from community.models import JoinRequest
from users.models import SystersUser


class UserView(LoginRequiredMixin, TemplateView):
    """User view"""
    template_name = "users/view_profile.html"

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        username = context['username']
        systersuser = get_object_or_404(SystersUser, user__username=username)
        communities = systersuser.communities.all()
        join_requests = JoinRequest.objects.filter(user=systersuser,
                                                   is_approved=False)
        context_dict = {'systersuser': systersuser,
                        'communities': communities,
                        'join_requests': join_requests}
        for key, value in context_dict.iteritems():
            context[key] = value
        return context
