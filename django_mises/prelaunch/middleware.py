# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.urlresolvers import resolve, reverse, NoReverseMatch

from django.conf import settings

from django_mises.prelaunch import views

class RequireAdminMiddleware(object):
    """Middleware blocking access to the site unless the user is an admin
    """

    def process_request(self, request):
        """Return None if all is ok, otherwise prompt login
        """

        if request.user.id and request.user.is_staff:
            return None
        else:
            func, args, kwargs = resolve(request.path)

            if settings.DEBUG:
                if kwargs.has_key('document_root'):
                    ## Pop hard-coded static kwarg for reversing
                    kwargs.pop('document_root')
                    try:
                        if request.path == reverse('serve', kwargs=kwargs):
                            return None
                    except NoReverseMatch, e:
                        pass

            if kwargs.has_key('invitation_secret'):
                return None
            elif kwargs.has_key('preview'):
                ## Pop also hard-coded preview keyword for reversing
                kwargs.pop('preview')
                if request.path == reverse('preview', kwargs=kwargs):
                    return None

        return views.admin_login(request)

# EOF

