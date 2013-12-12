import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'activity.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

path = '/group_project/activityappShaneCopy'
if path not in sys.path:
    sys.path.append(path)