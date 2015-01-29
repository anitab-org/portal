from django.conf.urls import url

from blog.views import (CommunityNewsListView, CommunityNewsView,
                        AddCommunityNewsView, EditCommunityNewsView,
                        DeleteCommunityNewsView, CommunityResourceListView,
                        CommunityResourceView, AddCommunityResourceView,
                        EditCommunityResourcesView,
                        DeleteCommunityResourceView)

urlpatterns = [
    url(r'^(?P<slug>\w+)/news/$', CommunityNewsListView.as_view(),
        name="view_community_news_list"),
    url(r'^(?P<slug>\w+)/news/add/$', AddCommunityNewsView.as_view(),
        name="add_community_news"),
    url(r'^(?P<slug>\w+)/news/(?P<news_slug>\w+)/edit/$',
        EditCommunityNewsView.as_view(), name="edit_community_news"),
    url(r'^(?P<slug>\w+)/news/(?P<news_slug>\w+)/delete/$',
        DeleteCommunityNewsView.as_view(), name="delete_community_news"),
    url(r'^(?P<slug>\w+)/news/(?P<news_slug>\w+)/$',
        CommunityNewsView.as_view(), name="view_community_news"),
    url(r'^(?P<slug>\w+)/resources/$', CommunityResourceListView.as_view(),
        name="view_community_resource_list"),
    url(r'^(?P<slug>\w+)/resources/add/$',
        AddCommunityResourceView.as_view(), name="add_community_resource"),
    url(r'^(?P<slug>\w+)/resources/(?P<resource_slug>\w+)/edit/$',
        EditCommunityResourcesView.as_view(), name="edit_community_resource"),
    url(r'^(?P<slug>\w+)/resources/(?P<resource_slug>\w+)/delete/$',
        DeleteCommunityResourceView.as_view(),
        name="delete_community_resource"),
    url(r'^(?P<slug>\w+)/resources/(?P<resource_slug>\w+)/$',
        CommunityResourceView.as_view(), name="view_community_resource"),
]
