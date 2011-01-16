# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models

from django.shortcuts import get_object_or_404, render_to_response

from django.template import RequestContext

from django_mises.blog import models as blog_models

def user_view(request, username):
    """View the user
    """

    import datetime

    user = get_object_or_404(auth_models.User, username=username, is_active=True)

    now = datetime.datetime.now()

    post_count = blog_models.Post.objects.filter(author=user, publish_at__lte=now).count()

    # Avoid template namespace clash
    context = {
        'viewed_user': user,
        'post_count': post_count,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('user.html', req_ctx)

# EOF

