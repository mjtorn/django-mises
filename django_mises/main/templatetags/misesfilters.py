# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django_mises.blog import models

from django.template import Library

import datetime

register = Library()

@register.inclusion_tag('tags/blog_preview.html')
def blog_preview():
    """Return a list of latest published blogs
    """

    now = datetime.datetime.now()

    posts = models.Post.objects.filter(publish_at__lte=now).select_related().order_by('-publish_at')[:10]

    return {
        'posts': posts,
    }

# EOF

