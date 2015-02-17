from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from common.views import IndexView
from common.views import AboutUsView

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    pass

urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^community/', include('blog.urls')),
    url(r'^community/', include('community.urls')),
    url(r'^community/', include('membership.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^about-us/$', AboutUsView.as_view(), name='about-us'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
