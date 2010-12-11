# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.conf.urls.defaults import *
from django.conf import settings

from main import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^/user/(?P<username>\w+)$', views.index, name='user'),
)

# EOF

