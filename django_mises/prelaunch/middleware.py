# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

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
            from django.core.urlresolvers import resolve
            func, args, kwargs = resolve(request.path)
            if kwargs.has_key('invitation_secret'):
                return None

        return views.admin_login(request)

# EOF

