from django.core.exceptions import ImproperlyConfigured

from community.constants import DEFAULT_COMMUNITY_ACTIVE_PAGE
from community.models import CommunityPage


class CommunityMenuMixin(object):
    """Mixin allows to add to the context information required to render the
    Community menu:

    * All community pages (CommunityPage objects) of a specific community
    * Current active page slug
    """
    community = None
    page = None

    def get_context_data(self, **kwargs):
        context = super(CommunityMenuMixin, self).get_context_data(**kwargs)
        community = self.get_community()
        pages = CommunityPage.objects.filter(community=community).\
            order_by('order')
        context['pages'] = pages

        page = self.get_page()
        if page:
            context['active_page'] = page.slug
        else:
            if pages:
                context['active_page'] = pages[0].slug
            else:
                context['active_page'] = DEFAULT_COMMUNITY_ACTIVE_PAGE
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

    def get_page(self):
        """Get a community page.

        :return: CommunityPage object
        """
        return self.page
