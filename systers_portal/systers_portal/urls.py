from django.conf.urls import patterns, include, url
from django.contrib import admin

from dashboard.views import edit_userprofile

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/(?P<username>[\w.@+-]+)/edit/$',
        edit_userprofile, name='edit_userprofile'),
    url(r'^', include('cms.urls')),
)
