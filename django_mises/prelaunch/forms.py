# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import forms as auth_forms

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

# EOF

