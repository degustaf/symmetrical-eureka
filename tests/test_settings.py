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
    'django.contrib.staticfiles',
    'SymmetricalEureka',
    'social.apps.django_app.default',
    'bootstrap3',
    'tests',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/SymmetricalEureka/templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
            'debug': True,
        },
    },
]

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
STATIC_ROOT = '/home/degustaf/symmetrical-eureka/SymmetricalEureka/static/'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

BOOTSTRAP3 = {
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
        'ability_scores':
            'SymmetricalEureka.renderers.AbilityScoreFieldRenderer',
        },
    }

# Social Auth Keys
SOCIAL_AUTH_FACEBOOK_KEY = 'test_Facebook_key'
SOCIAL_AUTH_FACEBOOK_SECRET = 'test_Facebook_secret'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'test_Google_key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'test_Google_secret'

SOCIAL_AUTH_TWITTER_KEY = 'test_twitter_key'
SOCIAL_AUTH_TWITTER_SECRET = 'test_twitter_secret'
