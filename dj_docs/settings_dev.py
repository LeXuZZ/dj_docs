import os
import redis

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_URL = "http://127.0.0.1:8000/"

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'precise',
            'filename': 'log/dj_docs.log',
            'maxBytes': 1024 * 1024 * 10  # 10 mb
        },
    },
    'loggers': {
        'DJ_DOCS_LOGGER': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'precise': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    }
}