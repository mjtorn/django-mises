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
    content = ckeditor_fields.RichTextField()

    publish_at = models.DateField(verbose_name=_('Publish at'), db_index=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated_at at'), auto_now=True)

    def get_absolute_url(self):
        return reverse('post', post_id=self.id, slug=self.slug)

    def __unicode__(self):
        return u'%s: %s' % (self.id, self.title)

# EOF

