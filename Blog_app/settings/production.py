from django.conf import settings

import dj_database_url

DEBUG = False

TEMPLATE_DEBUG = True

DATABASES = settings.DATABASES

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*']

