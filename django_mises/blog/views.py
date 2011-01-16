# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.template import RequestContext

from django.shortcuts import get_object_or_404, render_to_response

from blog import models as blog_models

def post(request, post_id, slug=None):
    """Index view
    """

    import datetime

    now = datetime.datetime.now()

    post = get_object_or_404(blog_models.Post, id=post_id, publish_at__lte=now)

    context = {
        'post': post,
        'title': post.title,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('post.html', req_ctx)

# EOF


