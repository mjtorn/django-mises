# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate, login

from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect

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

def register(request):
    """Registration view, Django offers none
    """

    data = request.POST.copy() or None

    user_creation_form = auth_forms.UserCreationForm(data)
    if user_creation_form.is_bound:
        if user_creation_form.is_valid():
            user = user_creation_form.save()

            user = authenticate(username=user.username, password=user_creation_form.cleaned_data['password1'])
            login(request, user)

            return HttpResponseRedirect(reverse('user', args=(user.username,)))

    context = {
        'user_creation_form': user_creation_form,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('register.html', req_ctx)

# EOF

