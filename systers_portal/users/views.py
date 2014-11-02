from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from braces.views import LoginRequiredMixin

from community.models import JoinRequest
from users.models import SystersUser


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
                        'communities': communities,
                        'join_requests': join_requests,
                        'permission_groups': permission_groups}
        for key, value in context_dict.iteritems():
            context[key] = value
        return context
