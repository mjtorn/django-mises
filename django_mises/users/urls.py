# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import views as auth_views

from django.contrib.flatpages import views as flatpages_views

from django.conf.urls.defaults import *
from django.conf import settings

from users import views

urlpatterns = patterns('',
    url(r'^user/(?P<username>[\w.@+-]+)$', views.user_view, name='user'),

    ## Plagiate this stuff from django
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
)

# EOF

