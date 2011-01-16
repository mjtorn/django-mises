# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models

from django.utils.translation import ugettext_lazy as _

from django.db import models

import hashlib

import random

import time

## The immutable principle on which all speculation is impossible
AUTHOR_GROUP = auth_models.Group.objects.get(name='Authors')

class Invitation(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=75, unique=True)

    user = models.ForeignKey(auth_models.User)

    secret = models.CharField(max_length=40)

    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True, default=None)

    def __unicode__(self):
        return '%s' % self.email

    def save(self, *args, **kwargs):
        if not self.id:
            from django.core import mail

            secret = '%s%s' % (str(random.random()).split('.')[1], str(time.time()).replace('.', ''))
            self.secret = hashlib.sha1(secret).hexdigest()

            user = auth_models.User()

            user.username = user.email = self.email
            user.first_name = self.first_name
            user.last_name = self.last_name

            # To access admin
            user.is_staff = True

            # But not yet
            user.is_active = False

            user.save()

            self.user = user

            super(Invitation, self).save(*args, **kwargs)

            user.groups.add(AUTHOR_GROUP)

            email = mail.EmailMessage(
                to = (user.email,),
                subject = _('Invitation to mises.fi'),
                body = """\
Hei!

Teidät on kutsuttu Suomen Ludwig von Mises -Instituutin sivuille.

Ystävällisesti klikatkaa linkkiä http://mises.fi/admin/invitation/%s asettaaksenne salasanan.
Käyttäjätunnus on sama kuin sähköpostinne.

Tervetuloa!

-- 
mises

                """ % self.secret
            )

            email.send()
        else:
            super(Invitation, self).save(*args, **kwargs)

# EOF

