# vim: tabstop=4 expandtab autoindent shiftwidth=4 fileencoding=utf-8

from django.core.management import call_command

from django.db import connections

def setup():
    for db in connections:
        if globals().has_key('fixtures'):
            call_command('loaddata', *globals()['fixtures'], **{'verbosity': 0, 'commit': False, 'database': db})



def teardown():
    for db in connections:
        call_command('flush', verbosity=0, interactive=False, database=db)

# EOF

