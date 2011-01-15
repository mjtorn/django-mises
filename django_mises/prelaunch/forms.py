# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models as auth_models

from django import forms

class AuthenticateAdminForm(auth_forms.AuthenticationForm):
    """Are we an admin trying to log in?
    """

    def clean(self, *args, **kwargs):
        """Validate user exists and then validate being admin
        """

        super(AuthenticateAdminForm, self).clean(*args, **kwargs)

        if self.user_cache is not None and not self.user_cache.is_staff:
            raise forms.ValidationError(_('User is not admin'))

        return self.cleaned_data


class UsernameForm(forms.Form):
    """Prompt for username
    """

    ## Copypasta courtesy of django
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            auth_models.User.objects.get(username=username)
        except auth_models.User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))


# EOF

