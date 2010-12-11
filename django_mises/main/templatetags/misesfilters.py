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

@register.inclusion_tag('tags/blog_nav.html', takes_context=True)
def blog_nav(context):
    """Required so we can test if we're the last blog entry
    """

    now = datetime.datetime.now()

    post = context['post']

    count = models.Post.objects.filter(publish_at__lte=now, id__gt=post.id).count()

    return {
        'has_previous': post.id > 1,
        'has_next': count > 0,
        'previous': post.id - 1,
        'next': post.id + 1,
    }

# EOF

