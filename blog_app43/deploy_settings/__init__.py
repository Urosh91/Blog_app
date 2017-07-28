from blog_app43.settings import *


DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '.herokuapp.com',
]

SECRET_KEY = get_env_variable('SECRET_KEY')
