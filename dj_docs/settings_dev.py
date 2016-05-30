import os
import redis

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/img')

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

redis_instance = redis.StrictRedis(**REDIS_CONFIG)