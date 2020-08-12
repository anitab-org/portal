from django.conf.urls import url

from users.views import UserView, UserProfileView
from users.views import EditSettings, UserPinsListView

from blog.views import RemovePinFromListView

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/$', UserView.as_view(), name='user'),
    url(r'^(?P<username>[\w.@+-]+)/profile/$', UserProfileView.as_view(),
        name='user_profile'),
    url(r'^(?P<username>[\w.@+-]+)/settings/$', EditSettings.as_view(),
        name="edit_settings"),
    url(r'^(?P<username>[\w.@+-]+)/mypins/$', UserPinsListView.as_view(),
        name="user_pins"),
    url(r'^(?P<username>[\w.@+-]+)/mypins/unpin.$', RemovePinFromListView.as_view(),
        name="user_unpin")
]
