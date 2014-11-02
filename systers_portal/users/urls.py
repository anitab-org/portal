from django.conf.urls import url

from users.views import UserView, UserProfileView


urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', UserView.as_view(), name='user'),
    url(r'^(?P<username>[\w.@+-]+)/profile/$', UserProfileView.as_view(),
        name='user_profile'),
]
