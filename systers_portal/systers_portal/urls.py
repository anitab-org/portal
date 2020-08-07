from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views
from django.views.static import serve

from common.views import IndexView, Logout
from common.views import ContactView
from common.views import AboutUsView
from common.views import NewCommunityProposalView

try:
    admin.autodiscover()
except admin.sites.AlreadyRegistered:
    pass

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^community/', include('blog.urls')),
    url(r'^community/', include('community.urls')),
    url(r'^community/', include('membership.urls')),
    url(r'^meetup/', include('meetup.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/', Logout.as_view(), name='logout'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/upload/', login_required(views),
        name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(login_required(views.browse)),
        name='ckeditor_browse'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^about-us/$', AboutUsView.as_view(), name='about-us'),
    url(r'^propose/newcommunity/$', NewCommunityProposalView.as_view(),
        name='new-community-proposal'),
    url(r'^notifications/', include('pinax.notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT}),
    ]
