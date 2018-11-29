from .base import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

INSTALLED_APPS += (
    'django_nose',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'systersdb',
        'USER': config('TEST_DB_USER'),
        'PASSWORD': config('TEST_DB_PASSWORD'),
        'HOST': config('TEST_DB_HOST', default='localhost'),
        'PORT': config('TEST_DB_PORT', default='5432'),
    }
}

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'systers_portal.systers_portal.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--nocapture',
    '--nologcapture',
    # '--with-doctest',
    # '--doctest-options=+ELLIPSIS',
]

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
