# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django import forms

from django.contrib import admin

from django_mises.blog import models

from ckeditor import widgets as ckeditor_widgets

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = models.Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'co_author', 'publish_at')
    list_filter = ('publish_at',)
    fieldsets = (
        (None, {
            'fields': ('co_author', 'title', 'content', 'publish_at')
        }),
    )

    form = PostAdminForm

    def queryset(self, request):
        qs = super(PostAdmin, self).queryset(request)
        if request.user.has_perm('blog.change_post') or request.user.has_perm('blog.can_edit') or request.user.has_perm('blog.can_publish'):
            return qs

        return qs.filter(author=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            if request.user.has_perm('blog.can_publish'):
                return ()
            elif request.user.has_perm('blog.can_edit'):
                return ('co_author', 'publish_at',)
            else:
                if obj is not None and request.user.id == obj.author.id:
                    readonly = ('publish_at',)
                elif obj is None:
                    readonly = ('publish_at',)
                else:
                    readonly = ('co_author', 'title', 'content', 'publish_at',)
                return readonly
        return ()

    def change_view(self, request, object_id, extra_context=None):
        """Deal with custom editing
        """

        from django_mises import comments

        data = request.POST.copy() or None

        obj = models.Post.objects.get(id=object_id)

        ## Handle our data, let the rest flow over
        comment_form = comments.get_internal_form()(obj, data)
        context = {
            'comment_form': comment_form,
        }

        if data is not None:
            if data.has_key('internal_comment'):

                if comment_form.is_bound:
                    if comment_form.is_valid():
                        ## Do not allow tampering
                        comment_form.cleaned_data['user'] = request.user

                        comment = comment_form.save()

        ## Maybe redirect out, maybe complain
        return super(PostAdmin, self).change_view(request, object_id, extra_context=context)

    def save_model(self, request, obj, form, change):
        from pytils.translit import slugify

        for f in obj._meta.fields:
            val = form.cleaned_data.get(f.name, None)
            if val:
                setattr(obj, f.name, val)

        if not hasattr(obj, 'author'):
            obj.author = request.user
        obj.slug = slugify(obj.title)

        obj.save()


admin.site.register(models.Post, PostAdmin)

# EOF

