# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.db import models

from django.contrib.admin.filterspecs import FilterSpec, DateFieldFilterSpec

from django.utils.encoding import smart_unicode

from django.utils.translation import ugettext_lazy as _

import datetime

class IsPublishedFilterSpec(DateFieldFilterSpec):
    """http://stackoverflow.com/questions/991926/custom-filter-in-django-admin
    """

    def __init__(self, f, request, params, model, model_admin):
        super(IsPublishedFilterSpec, self).__init__(f, request, params, model, model_admin)

        now = datetime.datetime.now()

        ## FIXME The date filters don't work too well
        self.links = (
            (_('Any'), {}),
            (_('Yes'), {
                '%s__isnull' % self.field.name: False,
                '%s__lte' % self.field.name: now.date(),
                'ot': 'asc',
                'o': '4',
            }),
            (_('No'), {
                '%s__isnull' % self.field.name: True,
            }),
            (_('Date set'), {
                '%s__isnull' % self.field.name: False,
                'ot': 'asc',
                'o': '4',
            }),
            (_('Coming'), {
                '%s__gt' % self.field.name: now.date(),
                'ot': 'asc',
                'o': '4',
            }),
        )

    def title(self):
        return _('Is published')

FilterSpec.filter_specs.insert(0, (lambda f: getattr(f, 'is_published_filter', None), IsPublishedFilterSpec))

# EOF

