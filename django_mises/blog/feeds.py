# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.urlresolvers import reverse

from django.contrib.syndication.views import Feed

from django.utils.translation import ugettext_lazy as _

from django.shortcuts import get_object_or_404

from blog import models as blog_models

import datetime

import time

class ArticlesFeed(Feed):
    """Mises articles
    """

    title = _('Mises articles')
    description = _('New articles on Mises')

    def get_object(self, request):
        """Inconceivable, but this does work o_O
        """
        bob = get_object_or_404(blog_models.Post, id=1)
        return bob

    def link(self, obj):
        return obj.get_absolute_url()

    def items(self):
        now = datetime.datetime.now()
        return blog_models.Post.objects.filter(publish_at__lte=now).select_related().order_by('-publish_at')

    def item_author_name(self, obj):
        return '%s %s' % (obj.author.first_name, obj.author.last_name)

    def item_author_link(self, obj):
        return reverse('user', args=(obj.author.username,))

    def item_pubdate(self, obj):
        return datetime.datetime.fromtimestamp(time.mktime(obj.publish_at.timetuple()))

    def item_title(self, obj):
        return obj.title

    def item_description(self, obj):
        return obj.preview

# EOF

