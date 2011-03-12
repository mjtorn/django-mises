# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms

from django.conf import settings

from django.contrib.contenttypes import models as contenttypes_models

from django.utils.encoding import force_unicode

from django.utils.translation import ugettext_lazy as _

from django_mises.comments import models

import cgi

import datetime

class TypedCommentBaseForm(forms.Form):
    """Common functionality for both internal and external forms
    """

    def __init__(self, target_object, data=None, initial=None):
        """Plagiated from reference form
        """

        self.target_object = target_object
        if initial is None:
            initial = {}

        super(TypedCommentBaseForm, self).__init__(data=data, initial=initial)

    def get_comment_model(self):
        return models.TypedComment

    def get_comment_create_data(self):
        """Tweak from reference implementation
        """

        # Removed user_name, email and url
        data = dict(
            content_type = contenttypes_models.ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            ## If the subclass form is external, internal_comment can never be in cleaned_data
            comment      = self.cleaned_data.get('internal_comment', self.cleaned_data.get('comment', None)),
            submit_date  = datetime.datetime.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
            ip_address   = self.cleaned_data.get('ip_address', None),
        )

        # Raise database error if this is missing
        data['user'] = self.cleaned_data.get('user', None)

        # Raise database error if this is not set in subclass method
        data['comment_type'] = None

        return data

    def save(self):
        comment = models.TypedComment()

        for key, value in self.get_comment_create_data().items():
            setattr(comment, key, value)

        ## Never trust user input
        split_comment = cgi.escape(comment.comment).splitlines()

        ## Ghetto indent and clean
        for i in xrange(len(split_comment)):
            if split_comment[i].startswith(' '):
                len_orig = len(split_comment[i])
                stripped = split_comment[i].lstrip()
                len_stripped = len(stripped)

                split_comment[i] = '%s%s' % ((len_orig - len_stripped) * '&nbsp;', stripped)

            split_comment[i] = split_comment[i].rstrip()

        ## Ghetto format
        new_comment = '<p>'
        new_comment = '%s%s' % (new_comment, '</p><p>'.join(split_comment))
        new_comment = '%s</p>' % new_comment

        comment.comment = new_comment

        comment.save()

        return comment

class InternalCommentForm(TypedCommentBaseForm):
    """To avoid (in this case) useless overhead in the reference implementation
    """

    internal_comment = forms.fields.CharField(label=_('Comment'), widget=forms.widgets.Textarea())

    def get_comment_create_data(self):
        data = super(InternalCommentForm, self).get_comment_create_data()

        data['comment_type'] = 'internal'

        return data

class ExternalCommentForm(TypedCommentBaseForm):
    """To avoid (in this case) useless overhead in the reference implementation
    """

    comment = forms.fields.CharField(label=_('Comment'), widget=forms.widgets.Textarea())

    def get_comment_create_data(self):
        data = super(ExternalCommentForm, self).get_comment_create_data()

        data['comment_type'] = 'external'

        return data

# EOF

