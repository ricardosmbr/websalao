"""
Django settings for salao project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "=d7$t)fhsla=-)l0qh%jz8%^00vm&2&r+wci7dc8l1lsivfare"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*",'http//:localhost:8050']


# Application definition


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "debug_toolbar",
    "import_export",
    "aplicacao",
    "configuracao",
    "events",
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "salao.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

GRAPHENE = {
    "SCHEMA": "aplicacao.schema.schema"
}

WSGI_APPLICATION = "salao.wsgi.application"


CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:8050',
)

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if os.getenv("DATABASE_NAME"):
    DATABASES = {
        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "HOST": os.getenv("DATABASE_HOST"),
        #     "PORT": os.getenv("DATABASE_PORT"),
        #     "USER": os.getenv("DATABASE_USER"),
        #     "PASSWORD": os.getenv("DATABASE_PASSWORD"),
        #     "NAME": os.getenv("DATABASE_NAME"),
        # }
 
        # # RDS Amazon
        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "HOST": "34.151.230.64",
        #     "PORT": 5432,
        #     "USER": "postgres",
        #     "PASSWORD": "Rsmi2402!!",
        #     "NAME": "salao",
        # }

        # ip 52.54.68.226
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "ec2-52-54-68-226.compute-1.amazonaws.com",
            "PORT": 5432,
            "USER": "pzdmwdvvgtgvcl",
            "PASSWORD": "3e271fe52a4dd7f769013859f2e1b26054608b9dbc368f5ee723002aaca9e2fc",
            "NAME": "df47toge9anrvv",
        }
    }
else:
    DATABASES = {
        # "default": {
        #     "ENGINE": "django.db.backends.sqlite3",
        #     "NAME": BASE_DIR / "db.sqlite3",
        # }

        # # RDS ec2-15-229-91-203.sa-east-1.compute.amazonaws.com (15.229.91.203) 
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "15.229.91.203",
            "PORT": 5432,
            "USER": "postgres",
            "PASSWORD": "Rsmi2402!!",
            "NAME": "salao",
        }

        # "default": {
        #     "ENGINE": "django.db.backends.postgresql",
        #     "HOST": "ec2-52-54-68-226.compute-1.amazonaws.com",
        #     "PORT": 5432,
        #     "USER": "pzdmwdvvgtgvcl",
        #     "PASSWORD": "3e271fe52a4dd7f769013859f2e1b26054608b9dbc368f5ee723002aaca9e2fc",
        #     "NAME": "df47toge9anrvv",
        # }

    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True
TIME_ZONE = "America/Sao_Paulo"
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    "static",
]
CELERY_BROKER_URL = "redis://h:TruQ6L0MfDmD6kc4lg5WhXEmTn1oeEKf@redis-10341.c212.ap-south-1-1.ec2.cloud.redislabs.com:10341"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "172.21.0.1",
    # ...
]
