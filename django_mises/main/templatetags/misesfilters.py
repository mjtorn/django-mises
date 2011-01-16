# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.urlresolvers import resolve, reverse

from django_mises.blog import models as blog_models

from django_mises.main import models as main_models

from django.template import Library

import datetime

register = Library()

@register.filter
def getitem(ob, item):
    """get item from ob
    """

    try:
        return ob[item]
    except (KeyError, IndexError):
        return None

@register.simple_tag
def random_slogan():
    """Get a random slogan
    """

    return main_models.Slogan.objects.all().order_by('?').values('slogan')[0]['slogan']

@register.inclusion_tag('tags/blog_preview.html')
def blog_preview():
    """Return a list of latest published blogs
    """

    now = datetime.datetime.now()

    posts = blog_models.Post.objects.filter(publish_at__lte=now).select_related().order_by('-publish_at')[:10]

    return {
        'posts': posts,
    }

@register.inclusion_tag('tags/blog_nav.html', takes_context=True)
def blog_nav(context):
    """Required so we can test if we're the last blog entry
    """

    now = datetime.datetime.now()

    post = context['post']

    count = blog_models.Post.objects.filter(publish_at__lte=now, id__gt=post.id).count()

    return {
        'has_previous': post.id > 1,
        'has_next': count > 0,
        'previous': post.id - 1,
        'next': post.id + 1,
    }

@register.inclusion_tag('tags/nav.html', takes_context=True)
def nav(context, viewname, descr):
    """Figure out the menu items
    """

    view, args, kwargs = resolve(context['request'].META['PATH_INFO'])

    rev_view_name = reverse(viewname)

    ## This should be considerably better in the next Django.
    if view.func_name == resolve(rev_view_name)[0].func_name:
        active = True
    else:
        active = False

    return {
        'active': active,
        'link': reverse(viewname),
        'descr': descr,
    }

# EOF

