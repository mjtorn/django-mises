# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth import login

from django_mises.prelaunch import forms

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

# EOF

