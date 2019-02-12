"""
Django settings for way_to_home project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EASY_WAY_DIR = os.path.abspath(os.path.join(BASE_DIR, '../easy_way_data'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_v%d$8q8a3+^mo)v3x-pnwmaqha5ssp*k0j)_t6*^h3$!t5cij'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

APPEND_SLASH = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'custom_user',
    'user_profile',
    'place',
    'way',
    'route',
    'notification',
    'home',
    'utils',
]

SESSION_COOKIE_HTTPONLY = False

AUTH_USER_MODEL = 'custom_user.CustomUser'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.login_required.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'way_to_home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'way_to_home.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'HOST': 'postgres',
        'NAME': 'postgres',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/public/')
]

# Required settings for authorization via google

CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8000/api/v1/user/signin_via_google'
AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'
SCOPE = ['openid', 'https://www.googleapis.com/auth/userinfo.email']
STATE = 'way_to_home'

# Required settings for sending email.

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'EMAIL_HOST_USER@gmail.com'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'DEFAULT_FROM_EMAIL'

# JWT Token required settings.

JWT_KEY = 'any secret word'
JWT_ALGORITHM = 'HS384'

# Required settings for telegram bot

TELEGRAM_BOT_TOKEN = 'TELEGRAM_BOT_TOKEN'

# Required setting for NEXMO

NEXMO_API_KEY = 'Nexmo API KEY'
NEXMO_API_SECRET = 'Nexmo API SECRET'

# Required setting for Google Maps API

GOOGLE_API_KEY = 'Google API key'

# Celery settings

CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672'
CELERY_IGNORE_RESULT = True
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Europe/Kiev'

DOMAIN = 'localhost:8000'

# Logger required settings.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': os.path.join('/var/log/', 'way_to_home.log')
        },
    },
    'loggers': {
        'way_to_home': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
    'formatters': {
        'default': {
            'format': '{levelname} {asctime} {pathname} line: {lineno:d} '
                      'message: {message}',
            'datefmt': '%d/%m/%Y %H:%M:%S',
            'style': '{'
        },
    },
}

try:
    from way_to_home.local_settings import *
except ImportError:
    pass
