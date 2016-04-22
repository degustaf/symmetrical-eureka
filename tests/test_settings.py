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

ROOT_URLCONF = 'SymmetricalEureka.urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'SymmetricalEureka',
    'tests',
)

CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'test_secrets.json')

STATIC_URL = '/static/'
STATIC_ROOT = '/home/degustaf/madlibs/static'
