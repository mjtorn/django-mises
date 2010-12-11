# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.conf.urls.defaults import *
from django.conf import settings

from blog import views as blog_views

urlpatterns = patterns('',
    url(r'^post/(?P<post_id>\d+)/(?P<slug>.+)$', blog_views.index, name='post'),
)

# EOF

