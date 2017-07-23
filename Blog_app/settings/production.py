from django.conf import settings

import dj_database_url

DEBUG = False

TEMPLATE_DEBUG = True

DATABASES = settings.DATABASES

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['*', 'evening-depths-74818.herokuapp.com', ]

