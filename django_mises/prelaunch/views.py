# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate, login
from django.contrib.auth import forms as auth_forms

from django.core.urlresolvers import reverse

from django_mises.prelaunch import forms
from django_mises.prelaunch import models

from django.conf import settings

from django.http import HttpResponseRedirect

from django.shortcuts import render_to_response

from django.template import RequestContext

import re

def admin_login(request, redirect_field_name=REDIRECT_FIELD_NAME):
    """Log in an admin user
    """

    data = request.POST.copy() or None

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    authenticate_admin_form = forms.AuthenticateAdminForm(data=data)
    if authenticate_admin_form.is_bound:
        if authenticate_admin_form.is_valid():
            ## Means we authenticated ok
            login(request, authenticate_admin_form.user_cache)

            ## Take a lot of this from Django
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                redirect_to = settings.LOGIN_REDIRECT_URL
                
            return HttpResponseRedirect(redirect_to)

    context = {
        'authenticate_admin_form': authenticate_admin_form, 
        redirect_field_name: redirect_to,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('admin_login.html', req_ctx)

def set_password(request, invitation_secret):
    """View for setting password
    """

    try:
        invitation = models.Invitation.objects.get(secret=invitation_secret, used_at__isnull=True)
    except models.Invitation.DoesNotExist:
        return HttpResponseRedirect('/')

    data = request.POST.copy() or None

    ## Hits the database to request user but do not care
    set_password_form = auth_forms.SetPasswordForm(invitation.user, data=data)
    username_form = forms.UsernameForm(data=data)
    if set_password_form.is_bound and username_form.is_bound:
        if set_password_form.is_valid() and username_form.is_valid():
            import datetime

            ## This data needs to be updated over the initial info
            invitation.user.is_active = True
            invitation.user.username = username_form.cleaned_data['username']

            ## Because of object references, this saves activity and username
            set_password_form.save()
            user = authenticate(username=invitation.user.username, password=set_password_form.cleaned_data['new_password1'])
            login(request, user)

            ## So future leaks of the secret do not matter
            invitation.used_at = datetime.datetime.now()
            invitation.save()

            return HttpResponseRedirect(reverse('admin:index'))

    context = {
        'username_form': username_form,
        'set_password_form': set_password_form,
    }
    req_ctx = RequestContext(request, context)

    return render_to_response('invitation_set_password.html', req_ctx)

# EOF

