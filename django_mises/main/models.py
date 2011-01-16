# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.db import models

class Slogan(models.Model):
    """Different small slogans to change on page loads
    """

    slogan = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%s' % self.slogan

# EOF

