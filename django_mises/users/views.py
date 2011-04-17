# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth.decorators import login_required

from django.contrib.auth import models as auth_models
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate, login

from django.core.urlresolvers import reverse

from django.contrib import messages

from django.http import HttpResponseRedirect

from django.shortcuts import get_object_or_404, render_to_response

from django.template import RequestContext

from django_mises.blog import models as blog_models

from django_mises.users import forms as users_forms

def user_view(request, username):
    """View the user
    """

    import datetime

    user = get_object_or_404(auth_models.User, username=username, is_active=True)

    now = datetime.datetime.now()

    post_count = blog_models.Post.objects.filter(author=user, publish_at__lte=now).count()

    # Needs verification?
    email_verification_form = None
    if request.user.id == user.id and not user.get_profile().is_verified:
        data = request.POST.copy() or None

        email_verification_form = users_forms.EmailVerificationForm(data=data)
        if email_verification_form.is_bound:
            email_verification_form.data['user'] = request.user
            if email_verification_form.is_valid():
                email_verification_form.save()

                messages.info(request, 'Tunnukessi on aktivoitu!')

                return HttpResponseRedirect(reverse('user', args=(request.user.username,)))

    # Avoid template namespace clash
    context = {
        'viewed_user': user,
        'post_count': post_count,
        'email_verification_form': email_verification_form,
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

@login_required
def get_verification_code(request):
    """Maybe ajaxify this in the future
    """

    if request.user.get_profile().is_verified:
        messages.info(request, 'Olet jo vahvistanut osoitteesi')
    else:
        request.user.get_profile().gen_verification_code()
        print request.user.get_profile().verification_code
        ## TODO: actually send email
        messages.info(request, 'Vahvistuskoodi on lähetetty sähköpostiisi')

    return HttpResponseRedirect(reverse('user', args=(request.user.username,)))

# EOF

