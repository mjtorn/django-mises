# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.urlresolvers import resolve, reverse
from django.core.urlresolvers import NoReverseMatch, Resolver404

from django.http import Http404

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

@register.inclusion_tag('tags/blog_post_list.html', takes_context=True)
def blog_post_list(context):
    """Return a list of latest published blogs
    """

    now = datetime.datetime.now()

    posts = blog_models.Post.objects.filter(publish_at__lte=now).select_related().order_by('-publish_at')

    context['posts'] = posts

    return context

@register.inclusion_tag('tags/blog_nav.html', takes_context=True)
def blog_nav(context):
    """Required so we can test if we're the last blog entry
    """

    post = context['post']

    prev_post = post.get_previous_post()
    next_post = post.get_next_post()

    return {
        'has_previous': prev_post is not None,
        'has_next': next_post is not None,
        'previous': prev_post.id if prev_post else None,
        'next': next_post.id if next_post else None,
    }

@register.inclusion_tag('tags/nav.html', takes_context=True)
def nav(context, viewname, descr):
    """Figure out the menu items
    """

    ## Tuple of func, args, kwargs
    ## Somewhat better in Django 1.3

    try:
        match = resolve(context['request'].META['PATH_INFO'])
    except Resolver404, e:
        return {
            'active': False,
            'link': reverse('index'),
            'descr': descr,
        }

    # It tries to match combos like index with {'url': '/info/'} that always fail
    try:
        rev_view_name = reverse(viewname, args=match[1], kwargs=match[2])
    except NoReverseMatch:
        rev_view_name = reverse(viewname, args=match[1])

    potential_match = resolve(rev_view_name)

    if match[0] == potential_match[0] and match[1] == potential_match[1] and match[2] == potential_match[2]:
        active = True
    else:
        active = False

    return {
        'active': active,
        'link': reverse(viewname),
        'descr': descr,
    }

# EOF

