"""
Django settings for dj_docs project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
import uuid
from os.path import abspath, basename, dirname, join, normpath

BASE_DIR = dirname(dirname(__file__))

if not os.path.isdir(os.path.join(BASE_DIR, 'log')):
    os.makedirs(os.path.join(BASE_DIR, 'log'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$01+2um7!gy9q(#%53r^4t_bt(t0c2edqq59=&l2cfj5ar0ps_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    from dj_docs.settings_dev import *
else:
    from dj_docs.settings_prod import *

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'poll_auth',
    'poll',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dj_docs.urls'

WSGI_APPLICATION = 'dj_docs.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

# Configure templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'auth/templates'),
            os.path.join(BASE_DIR, 'poll/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

X_FRAME_OPTIONS = 'DENY'

REGISTRATION_EXPIRATION_TIME = 60 * 60 * 24  # 1 day

AUTH_USER_MODEL = 'poll_auth.PollUser'

AUTHENTICATION_BACKENDS = (
    'poll_auth.backends.PollAuthBackend',
    'django.contrib.auth.backends.ModelBackend'
)

LOGIN_URL = '/auth/login/'

LOGIN_REDIRECT_URL = '/'

# Check redis
try:
    from redis.exceptions import ConnectionError
    redis_session.set("dummy", "dummy")
except ConnectionError:
    from django.core.exceptions import ImproperlyConfigured

    raise ImproperlyConfigured("Redis is not available")

SENDGRID_API_KEY = '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'

SENDGRID_URL = "https://api.sendgrid.com/v3/mail/send"

REGISTRATION_HASH_LENGTH = 50

RECOVERY_PASSWORD_LENGTH = 10

logger = logging.getLogger('DJ_DOCS')

APPLICATION_UUID = uuid.uuid4().__str__()
