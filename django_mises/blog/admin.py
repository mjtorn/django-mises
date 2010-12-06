# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms

from django.contrib import admin

from django_mises.blog import models

from ckeditor import widgets as ckeditor_widgets

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = models.Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'co_author', 'publish_at')
    fieldsets = (
        (None, {
            'fields': ('co_author', 'title', 'content', 'publish_at')
        }),
    )

    form = PostAdminForm

    def queryset(self, request):
        qs = super(PostAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        from pytils.translit import slugify

        for f in obj._meta.fields:
            val = form.cleaned_data.get(f.name, None)
            if val:
                setattr(obj, f.name, val)

        obj.author = request.user
        obj.slug = slugify(obj.title)

        obj.save()


admin.site.register(models.Post, PostAdmin)

# EOF

