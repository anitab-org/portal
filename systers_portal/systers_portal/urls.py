from django.conf.urls import patterns, include, url
from django.contrib import admin

from systers_portal import settings
# from systers_portal.systers_portal import settings

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    pass

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^users/(?P<username>[\w.@+-]+)/$',
        'dashboard.views.view_userprofile',
        name='view_userprofile'),
    url(r'^$', 'dashboard.views.index', name='index',),
    url(r'^', include('cms.urls')),
)

urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
     'serve',
     {'document_root': settings.base.MEDIA_ROOT}), )
