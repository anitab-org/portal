from django.conf.urls import patterns, include, url
from django.contrib import admin
# from systers_portal.systers_portal import settings
from systers_portal import settings
from dashboard.views import view_userprofile, edit_userprofile, index

admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^users/(?P<username>\w+)/$',
        view_userprofile, name='view_userprofile'),
    url(r'^users/(?P<username>\w+)/edit/$',
        edit_userprofile, name='edit_userprofile'),
    url(r'^$', index, name='index',),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^', include('cms.urls')),
)
urlpatterns += patterns(
    'django.views.static',
    (r'media/(?P<path>.*)',
     'serve',
     {'document_root': settings.base.MEDIA_ROOT}), )
