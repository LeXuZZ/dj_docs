import os

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
