from django.views.generic import DetailView
from community.models import Community


class ViewCommunityProfileView(DetailView):
    """Community profile view"""
    template_name = "community/view_profile.html"
    model = Community
