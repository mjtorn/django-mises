# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.http import HttpResponseRedirect

from django.template import RequestContext

from django.shortcuts import get_object_or_404, render_to_response

from blog import models as blog_models

from django_mises import comments

def post(request, post_id, slug=None, preview=False):
    """Index view
    """

    data = request.POST.copy() or None

    import datetime

    now = datetime.datetime.now()

    if preview:
        post = get_object_or_404(blog_models.Post, id=post_id, slug=slug)
    else:
        post = get_object_or_404(blog_models.Post, id=post_id, publish_at__lte=now)

    comments_ = comments.get_model().objects.for_model(post).select_related(depth=1).filter(comment_type='external').order_by('id')

    comment_form = comments.get_external_form()(post, data)

    if comment_form.is_bound:
        if comment_form.is_valid():
            ## Ensure the correct user
            comment_form.cleaned_data['user'] = request.user
            comment_form.save()

            return HttpResponseRedirect(request.META['PATH_INFO'])

    context = {
        'post': post,
        'title': post.title,
        'comments': comments_,
        'comment_form': comment_form,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('post.html', req_ctx)

# EOF


