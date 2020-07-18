from .base import *

SCHEDULER_AUTOSTART = True
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'systersdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INTERNAL_IPS = ('127.0.0.1',)

# Instead of sending out real email, during development the emails will be sent
# to stdout, where from they can be inspected.
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
FROM_EMAIL = os.environ.get('FROM_EMAIL')
