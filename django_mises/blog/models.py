# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models

from django.core.urlresolvers import reverse

from django.utils.translation import ugettext_lazy as _

from django.conf import settings

from django.db import models

from ckeditor import fields as ckeditor_fields

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(auth_models.User, verbose_name=_('Author'), related_name='author')
    co_author = models.ForeignKey(auth_models.User, null=True, blank=True, default=None, verbose_name=_('Co-Author'), related_name='coauthor')

    title = models.CharField(verbose_name=_('Title'), max_length=256)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=256)

    preview = models.TextField()
    preview_img = models.CharField(max_length=256, null=True, blank=True, default=None)
    content = ckeditor_fields.RichTextField()

    publish_at = models.DateField(verbose_name=_('Publish at'), db_index=True, null=True, blank=True, default=None)
    updated_at = models.DateTimeField(verbose_name=_('Updated_at at'), auto_now=True)

    class Meta:
        permissions = (
            ('can_publish', 'Can set a publishing date'),
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
        for p in pq(self.content)('p'):
            preview = pq(p).html()
            preview = preview.strip()
            if preview:
                self.preview = preview
                break

        ## Find image
        img_html = None
        for p in pq(self.content)('p'):
            if p is not None:
                # Returns None if not found
                img_src = pq(p)('img').attr('src')
                if img_src:
                    self.preview_img = img_src
                    break

        return super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s: %s: %s' % (self.id, self.title, self.get_preview_start().replace('\r\n', ' ').strip())

# EOF

