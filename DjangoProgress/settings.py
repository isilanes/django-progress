# Standard libs:
import os
import json

# You can specify multiple configuration files to be checked in order.
# The first one found will be used.
try_confs = [
    os.environ.get("DJANGO_PROGRESS_CONF", None),
    os.path.join(os.environ["HOME"], ".django-progress.json"),
    os.path.join("conf", "django-progress.json"),
]

for conf in try_confs:
    if conf and os.path.isfile(conf):
        with open(conf, 'r') as f:
            J = json.load(f)
        break

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = J['SECRET_KEY']
SECRET_KEY = "whatever"

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = J["DEBUG"]
DEBUG = True
#ALLOWED_HOSTS = J["ALLOWED_HOSTS"]
ALLOWED_HOSTS = ["*"]

# Application definition:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4',
] + ["gasolina", "ahorro", "books", "pesos"]
#] + J.get("MY_INSTALLED_APPS", [])

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoProgress.urls'

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_PATH, "templates")],
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

WSGI_APPLICATION = 'DjangoProgress.wsgi.application'


# Database:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django-progress',
        'USER': 'django',
        'HOST': 'localhost',
    }
}


# Password validation:
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


# Internationalization:
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files:
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "DjangoProgress", "static"),
]
