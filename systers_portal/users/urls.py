from django.conf.urls import url

from users.views import UserProfileView


urlpatterns = [
    url(r'(?P<username>[\w.@+-]+)/$', UserProfileView.as_view(),
        name='user_profile'),
]
