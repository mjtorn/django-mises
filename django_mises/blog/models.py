# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models

from django.contrib.contenttypes import generic

from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from django.db import models

from django_mises.comments import models as comments_models

from ckeditor import fields as ckeditor_fields

from django_mises import email_helpers

import filters

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(auth_models.User, verbose_name=_('Author'), related_name='author')
    co_author = models.ForeignKey(auth_models.User, null=True, blank=True, default=None, verbose_name=_('Co-Author'), related_name='coauthor')

    title = models.CharField(verbose_name=_('Title'), max_length=256)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=256)

    preview = models.TextField()
    preview_img = models.CharField(max_length=256, null=True, blank=True, default=None)
    content = ckeditor_fields.RichTextField(verbose_name=_('Content'))

    publish_at = models.DateField(verbose_name=_('Publish at'), db_index=True, null=True, blank=True, default=None)
    publish_at.is_published_filter = True

    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    comments = generic.GenericRelation(comments_models.TypedComment, object_id_field='object_pk')

    class Meta:
        permissions = (
            ('can_publish', 'Can set a publishing date'),
            ('can_edit', 'Can edit posts by others'),
        )

    def get_absolute_url(self):
        return reverse('post', kwargs={
            'post_id': self.id,
            'slug': self.slug,
        })

    def get_preview_url(self):
        return reverse('preview', kwargs={
            'post_id': self.id,
            'slug': self.slug,
        })

    def get_preview_start(self):
        tail = ''
        if len(self.preview) > 300:
            tail = '...'

        return '%s%s' % (self.preview[:300], tail)

    def save(self, *args, **kwargs):
        from pyquery import PyQuery as pq

        ## Based on the assumption ckeditor always uses paragraphs
        # Also skip if someone accidentally started with an empty p
        # Also find image
        img_html = None
        first = True
        self.preview = None
        self.preview_img = None
        for p in pq(self.content)('p') + pq(self.content)('div'):
            preview = pq(p).html()

            # Policy dictates reprints are noted with <em> tags at the start
            em = pq(preview)('em')
            if em:
                em_html = em.outerHtml()
                if not preview.replace(em_html, ''):
                    continue

            # At least once we have an unclosed <em> at the end
            preview = pq(preview).text().strip()
            if preview and not self.preview:
                self.preview = preview
                if self.preview_img:
                    break

            # Returns None if not found
            img = pq(p)('img')
            img_src = img.attr('src')
            if img_src:
                self.preview_img = img_src
                if first:
                    self.preview = self.preview.strip(img.outerHtml())
                break

            first = False

        ## Send only on new posts
        notify = not self.id

        super(Post, self).save(*args, **kwargs)

        if notify:
            subject = _('New post')
            ctx = {
                'post': self,
            }
            email_helpers.send_publishers_authors_email(subject, 'send_notification_new_post.txt', ctx)

    def __unicode__(self):
        return u'%s: %s: %s' % (self.id, self.title, self.get_preview_start().replace('\r\n', ' ').strip())

# EOF

