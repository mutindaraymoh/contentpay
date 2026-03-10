import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-gw!(3ebyyo+@6kqi-2p6+y+!=v2xfakaytpfgh&i@h(btetma1'

DEBUG = True

ALLOWED_HOSTS = ['https://contentpay.onrender.com/','localhost','127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'contentapp',
    'django_daraja',  # M-Pesa integration
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'contentpay.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'contentpay.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'b00gq80urdwhn0dvfgiy',
        'USER': 'ugtedckeutgwwhie',
        'PASSWORD': 'yixNA5LeKXBdSZmphBGX',
        'HOST': 'b00gq80urdwhn0dvfgiy-mysql.services.clever-cloud.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
            'connect_timeout': 60,
            'read_timeout': 60,
            'write_timeout': 60,
        },
        'CONN_MAX_AGE': 0,
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login/Logout URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# ===================== M-Pesa Configuration =====================

MPESA_ENVIRONMENT = 'sandbox'  # Change to 'production' for live

# Safaricom Developer Portal credentials (updated)
MPESA_CONSUMER_KEY = "ao3m7ca1WTNnCOfXjKOqxJEISRmNPZiQq1GwQr9OG3goh4yh"
MPESA_CONSUMER_SECRET = "1U1jffnQ5q8ApBAKdPlSgONdODDrnWnjs2Qi2iCdkscsdxCTA703fvmexQ6QX6k8"
MPESA_SHORTCODE = "174379"  # Test Paybill
MPESA_EXPRESS_SHORTCODE = "174379"
MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# Callback URL (use ngrok for development)
MPESA_SANDBOX_CALLBACK_URL = "https://tangela-hesperideous-temeka.ngrok-free.dev/api/callback/"
