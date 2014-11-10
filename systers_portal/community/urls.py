from django.conf.urls import url

from community.views import ViewCommunityProfileView

urlpatterns = [
    url(r'^(?P<slug>\w+)/profile/$', ViewCommunityProfileView.as_view(),
        name='view_community_profile'),
]
