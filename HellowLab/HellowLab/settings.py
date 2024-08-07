"""
Django settings for HellowLab project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lyx6a7p7p59(g6j)uia#-i8f26708^q8%_lz*sb7kn)@k(^di!'

# SECURITY WARNING: don't run with debug turned on in production!
# Check if DEBUG_BOOL environment variable exists
if 'DEBUG_BOOL' in os.environ:
    # print("DEBUG_BOOL exists, use its value to set DEBUG")
    # DEBUG_BOOL exists, use its value to set DEBUG
    DEBUG = os.environ.get('DEBUG_BOOL').lower() == 'true'
else:
    # print("DEBUG_BOOL does not exist, default to True")
    # DEBUG_BOOL does not exist, default to True
    DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # everything below was added
    "corsheaders",
    "authentication.apps.AuthenticationConfig", 
    "rest_framework", 
    "rest_framework.authtoken", 
    "rest_framework_simplejwt", 
    "allauth", 
    "allauth.account", 
    "allauth.socialaccount",  # add if you want social authentication
    "dj_rest_auth",
    "dj_rest_auth.registration",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'HellowLab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'), 
            os.path.join(BASE_DIR, 'allauth'),
            os.path.join(BASE_DIR, 'templates', 'account')
        ],
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

WSGI_APPLICATION = 'HellowLab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Everything below was added #
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": "complexsigningkey",  # generate a key and replace me
    "ALGORITHM": "HS512",
}

SITE_ID = 1  # make sure SITE_ID is set


ACCOUNT_EMAIL_REQUIRED = True # old value false
ACCOUNT_EMAIL_VERIFICATION = "optional" #old value none

if DEBUG: # for testing, don't send an email, print to console.
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else: # use real smtp server
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # Gmail SMTP port
EMAIL_USE_TLS = True  # Transport Layer Security
EMAIL_HOST_USER = 'mango23322@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'plstetjhsbjanhbq'  # Your Gmail password or app password

# <EMAIL_CONFIRM_REDIRECT_BASE_URL>/<key>
EMAIL_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/login/email/confirm/"

# <PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL>/<uidb64>/<token>/
PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL = \
    "http://localhost:3000/login/password-reset/confirm/"

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_HTTPONLY": False,
    "PASSWORD_RESET_SERIALIZER": "dj_rest_auth.serializers.PasswordResetSerializer",

}

# CSRF_TRUSTED_ORIGINS=['http://127.0.0.1:8000', 'http://localhost:8000', 'http://tags.mangoon.duckdns.org', 'http://tags-backend.mangoon.duckdns.org', 'http://nextjs_tags:3000', 'http://localhost:3000', 'http://*']
CSRF_TRUSTED_ORIGINS=['http://127.0.0.1:8000', 'http://localhost:8000', 'http://tags.mgbcengineering.com', 'http://tagsdnekcab.mgbcengineering.com', 'http://mgbcengineering.com', 'https://tags.mgbcengineering.com', 'https://tagsdnekcab.mgbcengineering.com', 'https://mgbcengineering.com', 'http://nextjs_tags:3000', 'http://localhost:3000', 'http://*']

if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS=True
    # CSRF_TRUSTED_ORIGINS = ['tags-backend.mangoon.duckdns.org', 'tags.mangoon.duckdns.org', '127.0.0.1', 'localhost'] // use vesion in line 167
    # CORS_ALLOWED_ORIGINS = [
    #     "http://localhost:3000/",
    #     "http://127.0.0.1:3000/",
    #     "http://nextjs_tags:3000/"
    # ]

# AUTH_USER_MODEL = 'authentication.CustomUser'

ACCOUNT_ADAPTER = 'authentication.adapter.DefaultAccountAdapterCustom'
SITE_NAME = 'HellowLab'

if DEBUG:
    URL_FRONT = 'http://localhost:3000/'
else:
    URL_FRONT = 'https://tags.mgbcengineering.com/'
