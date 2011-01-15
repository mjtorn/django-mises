# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.conf.urls.defaults import *
from django.conf import settings

from prelaunch import views

urlpatterns = patterns('',
    url(r'^admin/invitation/(?P<invitation_secret>[a-z0-9]{40})$', views.set_password, name='invitation_set_password'),
)

# EOF

