# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

import settings

DEBUG = True
TEMPLATE_DEBUG = True

DEFAULT_FROM_ADDRESS = 'staff@mises.fi'

settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
settings.DATABASES['default']['NAME'] = '/home/mjt/src/git_checkouts/django-mises/mises.db'

MEDIA_ROOT = '/home/mjt/src/git_checkouts/django-mises/django_mises/media/'

CKEDITOR_UPLOAD_PATH = '%supload/' % MEDIA_ROOT

TIME_ZONE = 'Europe/Helsinki'

USE_L10N = True
LANGUAGE_CODE = 'fi'

DATE_FORMAT = 'l j.m.Y.'
TIME_FORMAT = 'h:i'
DATETIME_FORMAT = 'j.m.Y. h:i'

# EOF

