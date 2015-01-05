from django.conf.urls import url

from blog.views import CommunityNewsListView

urlpatterns = [
    url(r'^(?P<slug>\w+)/news/$', CommunityNewsListView.as_view(),
        name="view_community_news_list"),
]
