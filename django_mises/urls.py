from django.conf.urls.defaults import *

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('django_mises.main.urls')),
    (r'^', include('django_mises.blog.urls')),
    (r'^', include('django_mises.users.urls')),
    (r'^', include('django_mises.prelaunch.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^ckeditor/', include('ckeditor.urls')),

)

handler404 = 'django_mises.main.views.handler404'
handler500 = 'django_mises.main.views.handler500'

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}, name='serve')
    )

