from django.conf.urls import patterns, url
from dashboard import views
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'index/$', views.index, name='index'),
                       url(r'^profile/(?P<user_name_url>\w+)/$',
                           views.profiles, name='profiles'),
                       url(r'^edit_profile/$', views.edit_profile,
                           name='editprofile'),
                       url(r'^community/(?P<community_name_url>\w+)/$',
                           views.community, name='community'),
                       )
