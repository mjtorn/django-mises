# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.comments.managers import CommentManager

from django.conf import settings

from django.contrib.auth import models as auth_models

from django.contrib.comments import models as comments_models

from django.utils.translation import ugettext_lazy as _

from django.db import models

from django_mises import email_helpers

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

    def save(self, *args, **kwargs):
        notify = not self.id

        super(TypedComment, self).save(*args, **kwargs)

        if notify:
            post = self.content_object
            ctx = {
                'comment': self,
                'post': post,
            }

            # Internal comments go to publishers and editors
            if self.comment_type == 'internal':
                subject = _('New internal comment')
                email_helpers.send_publishers_authors_email(subject, 'send_notification_new_int_comment.txt', ctx)
            else:
                subject = _('New comment')

                ## Improbable generic foreign key filters would work
                users = set([post.author])

                if post.co_author:
                    users.add(post.co_author)

                commentators = auth_models.User.objects.filter(id__in=set([p.user.id for p in post.comments.all()]))
                for commentator in commentators:
                    users.add(commentator)

                for user in users:
                    email_helpers.send_user_email(user, subject, 'send_notification_new_ext_comment.txt', ctx)

    def __unicode__(self):
        return '%s: %s...' % (self.comment_type, self.comment[:100])

# EOF

