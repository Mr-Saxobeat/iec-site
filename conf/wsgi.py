"""
WSGI config for conf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

BASE_DIR2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# add the project path into the sys.path
sys.path.append('/var/www/html/iec-site/')

# add the virtualenv path to the sys.path
sys.path.append('/var/www/html/iec-site/.venv/lib/python3.8/site-packages/')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

application = get_wsgi_application()
