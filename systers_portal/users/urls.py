from django.conf.urls import url

from users.views import UserView


urlpatterns = [
    url(r'(?P<username>[\w.@+-]+)/$', UserView.as_view(), name='user'),
]
