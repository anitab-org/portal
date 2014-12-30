from django.core.exceptions import ImproperlyConfigured

from users.models import SystersUser


class UserDetailsMixin(object):
    """Mixin allows to add to the context information about the request user:

    * Is user member of the community
    * User join request to the community
    """
    community = None

    def get_context_data(self, **kwargs):
        context = super(UserDetailsMixin, self).get_context_data(**kwargs)
        user = self.request.user
        if user.username:
            community = self.get_community()
            systers_user = SystersUser.objects.get(user=user)
            context['is_member'] = systers_user.is_member(community)
            context['join_request'] = systers_user.get_last_join_request(
                community)
        return context

    def get_community(self):
        """Get a Community object.

        :return: Community object
        :raises ImproperlyConfigured: if Community is set to None
        """
        if self.community is None:
            raise ImproperlyConfigured(
                '{0} is missing a community property. Define {0}.community '
                'or override {0}.get_community()'
                .format(self.__class__.__name__)
            )
        return self.community
