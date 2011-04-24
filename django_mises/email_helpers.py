# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import template

from mailer import send_mail

from django.conf import settings

from django.contrib.auth import models as auth_models

from django.contrib.sites import models as sites_models

from django.db.models import Q

from django.utils.translation import ugettext_lazy as _

def render(context, template_name):
    tmpl = template.loader.get_template(template_name)

    return tmpl.render(template.Context(context))

def send(subject, to, template_name, extractx):
    """Generic mailer
    """

    site = sites_models.Site.objects.get_current()

    ## Email in our production is sent in English
    ## not worth debugging, easier to have language-specific templates
    # email is implied and language is explicit
    template_name = 'email/%s/%s' % (settings.LANGUAGE_CODE, template_name)

    ctx = {
        'site': site,
    }

    ctx.update(extractx)

    subject = '[%s] %s' % (site.domain, subject)
    body = render(ctx, template_name)

    send_mail(subject, body, settings.DEFAULT_FROM_ADDRESS, to)

def send_user_email(user, subject, template_name, context=None):
    """Email the verification code
    """

    if context is None:
        context = {}

    context['user'] = user

    to = (user.email,)

    send(subject, to, template_name, context)

def send_publishers_authors_email(subject, template_name, context=None):
    """Send email to publishers and authors
    No "to" argument required because of this
    """

    if context is None:
        context = {}

    qry = Q(groups__name='Publishers') | Q(groups__name='Editors')

    emails = auth_models.User.objects.filter(qry, is_active=True).distinct().values('email')
    to = [e['email'] for e in emails]

    send(subject, to, template_name, context)

# EOF

