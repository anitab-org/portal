from .base import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'systersdb',
        'USER': config('DEV_DB_USER'),
        'PASSWORD': config('DEV_DB_PASSWORD'),
        'HOST': config('DEV_DB_HOST', default='localhost'),
        'PORT': config('DEV_DB_PORT', default=5432),
    }
}

INTERNAL_IPS = ('127.0.0.1',)

# Instead of sending out real email, during development the emails will be sent
# to stdout, where from they can be inspected.
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
