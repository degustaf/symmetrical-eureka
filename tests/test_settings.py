"""
This is a Docstring.
"""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase'
        }
    }

SECRET_KEY = 'fake-key'

ROOT_URLCONF = 'SymmetricalEurekas.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_sample.plus',
    'SymmetricalEurekas',
    'tests',
)

STATIC_URL = '/static/'
STATIC_ROOT = '/home/degustaf/madlibs/static'
