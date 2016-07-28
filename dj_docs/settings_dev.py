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

redis_session = redis.StrictRedis(**REDIS_CONFIG)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s - %(name)s - %(levelname)s %(APPLICATION_UUID)s ] - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'filename': 'log/dj_docs.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 mb
            'backupCount': 10,
            'filters': ['application_id_filter']
        },
    },
    'filters': {
        'application_id_filter': {
            '()': 'util.logging.filter.ApplicationUUIDFilter'
        }
    },
    'loggers': {
        'DJ_DOCS': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
