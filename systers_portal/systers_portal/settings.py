"""
Django settings for systersPTL project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
gettext = lambda s: s
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p1e45+i2bgw^!eo6bdwkkyjsadtmki%g&@iz7je6f1tqcwqp+-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'django.contrib.sites',
		'cms',
		'mptt', 
		'menus',
		'south', 
		'sekizai', 
		)

MIDDLEWARE_CLASSES = (
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
#	'cms.middleware.multilingual.MultilingualURLMiddleware',
		'cms.middleware.page.CurrentPageMiddleware',
		'cms.middleware.user.CurrentUserMiddleware',
		'cms.middleware.toolbar.ToolbarMiddleware',
		)

TEMPLATE_CONTEXT_PROCESSORS = (
		'django.contrib.auth.context_processors.auth',
		'django.core.context_processors.i18n',
		'django.core.context_processors.request',
		'django.core.context_processors.media',
		'django.core.context_processors.static',
		'cms.context_processors.media',
		'sekizai.context_processors.sekizai',
		)


ROOT_URLCONF = 'systers_portal.urls'

WSGI_APPLICATION = 'systers_portal.wsgi.application'


TEMPLATE_DIRS = (
		    # The docs say it should be absolute path: PROJECT_PATH is precisely one.
		    # Life is wonderful!
		    os.path.join(BASE_DIR, "templates"),
		)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'systersdb',
		'USER': '',
		'PASSWORD': '',
		'HOST': 'localhost',
		'PORT': '5432',
	}
}
INTERNAL_IPS = ('127.0.0.1',)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('en-us', 'English'),
    ]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
ADMIN_MEDIA_PREFIX = "/static/admin/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

SITE_ID=1
