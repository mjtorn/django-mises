# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.contrib.sites.models import Site

def current_site(request):
    return {'site': Site.objects.get_current()}

# EOF

