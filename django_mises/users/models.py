# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models

from django.db import models

import hashlib

import random

import time

class UserProfile(models.Model):
    """Profile model
    """

    user = models.OneToOneField(auth_models.User)

    verification_code = models.CharField(max_length=40, null=True, blank=True, default=None)
    is_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s\'s profile' % self.user.username

    def gen_verification_code(self):
        """Generate code if it does not exist
        """

        if self.verification_code:
            return self.verification_code
        else:
            # Secure enough ;)
            timebase = str(time.time() / 10000000000).split('.')[1]
            randbase = str(random.random()).split('.')[1]
            base = '%s%s%s' % (timebase, self.user.email, randbase)

            self.verification_code = hashlib.sha1(base).hexdigest()

            self.save()

            return self.verification_code

def userprofile_creator(sender, instance, created, **kwargs):
    """Create a profile if none exists
    """

    if created:
        UserProfile.objects.create(user_id=instance.id)

models.signals.post_save.connect(userprofile_creator, sender=auth_models.User, dispatch_uid='userprofile_creation')

# EOF

