from .base import *
from decouple import config

SCHEDULER_AUTOSTART = True
DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='systersdb'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int),
    }
}

INTERNAL_IPS = ('127.0.0.1',)

# Instead of sending out real email, during development the emails will be sent
# to stdout, where from they can be inspected.
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_EMAIL = os.environ.get('FROM_EMAIL')
