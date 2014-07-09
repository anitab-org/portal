from django.conf.urls import patterns
from django.conf.urls import url
from dashboard import views
urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       )
