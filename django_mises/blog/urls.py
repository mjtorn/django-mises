# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.conf.urls.defaults import *
from django.conf import settings

from blog import views as blog_views
from blog import feeds as blog_feeds

urlpatterns = patterns('',
    url(r'^post/(?P<post_id>\d+)/(?P<slug>.+)/preview$', blog_views.post, {'preview': True}, name='preview'),
    url(r'^post/(?P<post_id>\d+)/(?P<slug>.+)$', blog_views.post, name='post'),
    url(r'^post/(?P<post_id>\d+)$', blog_views.post, name='post'),

    url(r'^rss.xml$', blog_feeds.ArticlesFeed()),
    # compatibility
    url(r'^dailyarticles.xml$', blog_feeds.ArticlesFeed()),
)

# EOF

