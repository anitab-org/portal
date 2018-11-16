from django.views.generic import TemplateView
from django.views.decorators.cache import cache_control
from allauth.account.views import LogoutView


class IndexView(TemplateView):
    template_name = "common/index.html"


class ContactView(TemplateView):
    template_name = "common/contact.html"


class AboutUsView(TemplateView):
    template_name = "common/about_us.html"


class NewCommunityProposalView(TemplateView):
    template_name = "common/new_community_proposal.html"


class Logout(LogoutView):

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
