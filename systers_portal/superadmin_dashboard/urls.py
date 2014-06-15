from django.conf.urls import patterns, url
from superadmin_dashboard import views
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'index/$', views.index, name='index'),
                       url(r'^add_community/$', views.add_community,
                           name='add_community'),
                       url(r'^edit_communityprofile/(?P<community_name_url>\w+)$',
                           views.edit_communityprofile, name='edit_communityprofile'),
                       url(r'^ShowCommunities/$',
                           views.ShowCommunities, name='ShowCommunities'),
                       )
