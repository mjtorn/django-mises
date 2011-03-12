# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django_mises.comments import forms
from django_mises.comments import models

def get_model():
    return models.TypedComment

def get_internal_form():
    return forms.InternalCommentForm

def get_external_form():
    return forms.ExternalCommentForm

# EOF

