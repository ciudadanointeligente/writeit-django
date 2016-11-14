#!/usr/bin/env python
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'testing_settings'

from django.core.management import call_command

def runtests():
    call_command('test','writeit')

try:
    import django
    setup = django.setup
except AttributeError:
    pass
else:
    setup()


if __name__ == '__main__':
    runtests()
    sys.exit(0)
