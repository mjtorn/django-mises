# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.auth import models as auth_models

from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from django.db import models

from django_mises.prelaunch import models as mises_models

from django import forms

class InvitationAdminForm(forms.ModelForm):
    class Meta:
        model = mises_models.Invitation

    def clean_email(self):
        email = self.data['email']
        try:
            # Because django authenticates by username, username is email
            auth_models.User.objects.get(username=email)
            raise forms.ValidationError(_('Found user for email'))
        except auth_models.User.DoesNotExist:
            return email


class InvitationAdmin(admin.ModelAdmin):
    form = InvitationAdminForm

    def get_readonly_fields(self, request, obj=None):
        """What are we not allowed to edit
        """

        return ('user', 'secret', 'created_at', 'used_at')


admin.site.register(mises_models.Invitation, InvitationAdmin)

# EOF

