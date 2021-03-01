"""
WSGI config for google_check project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_check.settings')

application = get_wsgi_application()


import os
import sys #Add this

from django.core.wsgi import get_wsgi_application
sys.path.append('/home/pbnpenal/public_html/') #Add this also
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_check.settings')


application = get_wsgi_application()
