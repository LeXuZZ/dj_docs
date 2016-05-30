import os
import redis

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ALLOWED_HOSTS = ["http://128.199.51.34/", "128.199.51.34"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dj_docs',  # path to DB
        'USER': 'postgres',  # User
        'PASSWORD': '',  # Password
        'HOST': 'localhost',  # localhost
        'PORT': '',  # '' means use default
    }
}

redis_instance = redis.Redis(unix_socket_path='/var/run/redis/redis.sock')