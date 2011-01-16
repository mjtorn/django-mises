# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.flatpages import views as flatpages_views

from django.conf.urls.defaults import *
from django.conf import settings

from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^info/$', flatpages_views.flatpage, {'url': '/info/'}, name='info'),
)

# EOF

