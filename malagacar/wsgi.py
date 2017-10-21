"""
WSGI config for malagacar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "malagacar.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "malagacar.settings.prod_settings")

# load secret variables. File is not to find at the repository!
SECRETS_FILE = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'malagacar/settings/secrets.py')
exec(open(SECRETS_FILE).read())

application = get_wsgi_application()
