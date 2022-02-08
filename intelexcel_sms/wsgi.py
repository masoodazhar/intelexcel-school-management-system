"""
WSGI config for intelexcel_sms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see the docs
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
""" 

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intelexcel_sms.settings')

application = get_wsgi_application()
