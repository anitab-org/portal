from django.conf.urls import url

from blog.views import CommunityNewsListView, CommunityNewsView

urlpatterns = [
    url(r'^(?P<slug>\w+)/news/$', CommunityNewsListView.as_view(),
        name="view_community_news_list"),
    url(r'^(?P<slug>\w+)/news/(?P<news_slug>\w+)/$',
        CommunityNewsView.as_view(), name="view_community_news"),
]
