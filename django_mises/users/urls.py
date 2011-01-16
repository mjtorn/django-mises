# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.flatpages import views as flatpages_views

from django.conf.urls.defaults import *
from django.conf import settings

from users import views

urlpatterns = patterns('',
    url(r'^user/(?P<username>[\w.@+-]+)$', views.user_view, name='user'),
)

# EOF

