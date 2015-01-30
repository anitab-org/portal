from django.conf.urls import url

from community.views import (CommunityLandingView, EditCommunityProfileView,
                             ViewCommunityProfileView, CommunityPageView,
                             AddCommunityPageView)

urlpatterns = [
    url(r'^(?P<slug>\w+)/$', CommunityLandingView.as_view(),
        name='view_community_landing'),
    url(r'^(?P<slug>\w+)/profile/$', ViewCommunityProfileView.as_view(),
        name='view_community_profile'),
    url(r'^(?P<slug>\w+)/profile/edit/$', EditCommunityProfileView.as_view(),
        name='edit_community_profile'),
    url(r'^(?P<slug>\w+)/p/add/$',
        AddCommunityPageView.as_view(), name="add_community_page"),
    url(r'^(?P<slug>\w+)/p/(?P<page_slug>\w+)/$',
        CommunityPageView.as_view(), name="view_community_page")
]
