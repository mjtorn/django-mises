# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.comments.managers import CommentManager

from django.conf import settings

from django.contrib.auth import models as auth_models

from django.contrib.comments import models as comments_models

from django.utils.translation import ugettext_lazy as _

from django.db import models

COMMENT_MAX_LENGTH = getattr(settings,'COMMENT_MAX_LENGTH', 3000)

class TypedComment(comments_models.BaseCommentAbstractModel):
    """Custom typed comment, similar to reference but forces user and adds type
    """

    user = models.ForeignKey(auth_models.User, verbose_name=_('User'), related_name='%(class)s_comments')
    comment_type = models.CharField(max_length=8, verbose_name=_('Type'))

    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)

    submit_date = models.DateTimeField(_('date/time submitted'), default=None)
    ip_address  = models.IPAddressField(_('IP address'), blank=True, null=True)
    is_public   = models.BooleanField(_('is public'), default=True,
                    help_text=_('Uncheck this box to make the comment effectively ' \
                                'disappear from the site.'))
    is_removed  = models.BooleanField(_('is removed'), default=False,
                    help_text=_('Check this box if the comment is inappropriate. ' \
                                'A "This comment has been removed" message will ' \
                                'be displayed instead.'))

    objects = CommentManager()

    def __unicode__(self):
        return '%s: %s...' % (self.comment_type, self.comment[:100])

# EOF

