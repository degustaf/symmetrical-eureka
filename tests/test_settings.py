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
    'SymmetricalEureka',
    'social.apps.django_app.default',
    'tests',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

STATIC_URL = '/static/'
STATIC_ROOT = '/home/degustaf/madlibs/static'

LOGIN_REDIRECT_URL = '/'

# Social Auth Keys
SOCIAL_AUTH_FACEBOOK_KEY = 'test_Facebook_key'
SOCIAL_AUTH_FACEBOOK_SECRET = 'test_Facebook_secret'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'test_Google_key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'test_Google_secret'

SOCIAL_AUTH_TWITTER_KEY = 'test_twitter_key'
SOCIAL_AUTH_TWITTER_SECRET = 'test_twitter_secret'
