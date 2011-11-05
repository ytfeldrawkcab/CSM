import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'owners.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/srv/django/owners'
if path not in sys.path:
    sys.path.append(path)
