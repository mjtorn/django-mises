# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import template

from django.core import mail

from django.contrib.sites import models as sites_models

from django.utils.translation import ugettext_lazy as _

def render(context, template_name):
    tmpl = template.loader.get_template(template_name)

    return tmpl.render(template.Context(context))

def send_user_email(user, template_name):
    """Email the verification code
    """

    ## Localization breaks
    ## http://code.djangoproject.com/ticket/6368
    site = sites_models.Site.objects.get_current()

    ctx = {
        'site_domain': site.domain,
        'site_name': site.name,
        'user': user,
        'user_first_name': user.first_name,
        'user_last_name': user.last_name,
        'user_username': user.username,
    }

    to = (user.email,)
    subject = _('Verification code for %s') % site.name

    body = render(ctx, template_name)

    message = mail.message.EmailMessage(to=to, subject=subject, body=body)

    message.send()

# EOF

