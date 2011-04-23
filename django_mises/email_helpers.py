# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import template

from mailer import send_mail

from django.conf import settings

from django.contrib.sites import models as sites_models

from django.utils.translation import ugettext_lazy as _

def render(context, template_name):
    tmpl = template.loader.get_template(template_name)

    return tmpl.render(template.Context(context))

def send_user_email(user, template_name, **extractx):
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

    ctx.update(extractx)

    to = (user.email,)
    subject = _('Verification code for %s') % site.name

    body = render(ctx, template_name)

    send_mail(subject, body, settings.DEFAULT_FROM_ADDRESS, to)

# EOF

