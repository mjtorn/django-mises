# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from annoying import decorators

from django.utils.translation import ugettext_lazy as _

from django import forms

@decorators.autostrip
class EmailVerificationForm(forms.Form):
    verification_code = forms.CharField(label=_('Verification code'), max_length=40)

    def clean_verification_code(self):
        if self.data['verification_code'] != self.data['user'].get_profile().verification_code:
            raise forms.ValidationError(_('Invalid verification code'))

        return self.data['verification_code']

    def save(self):
        self.data['user'].get_profile().is_verified = True
        self.data['user'].get_profile().save()
        print 'ok'

# EOF

