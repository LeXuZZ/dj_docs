import os
import redis

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_URL = "http://128.199.51.34/"

ALLOWED_HOSTS = ["http://128.199.51.34/", "128.199.51.34"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',  # path to DB
        'USER': 'django',  # User
        'PASSWORD': 'pNFb4ufATt',  # Password
        'HOST': 'localhost',  # localhost
        'PORT': '',  # '' means use default
    }
}

redis_instance = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')

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