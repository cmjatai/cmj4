from pathlib import Path
from decouple import AutoConfig
from dj_database_url import parse as db_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

config = AutoConfig(search_path=PROJECT_DIR)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

FOLDER_DEBUG_CONTAINER = Path(config('FOLDER_DEBUG_CONTAINER', default=__file__, cast=str))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_extensions',

    "django_vite",
    'django_celery_beat',
    'django_celery_results',

    "cmj4.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "cmj4.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "_templates"],
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

ASGI_APPLICATION = "cmj4.asgi.application"
WSGI_APPLICATION = "cmj4.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL_DEV' if DEBUG else 'DATABASE_URL_PRD',
        cast=db_url,
    )
}



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [PROJECT_DIR / "_frontend"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Where ViteJS assets are built.
DJANGO_VITE_ASSETS_PATH = PROJECT_DIR / "_frontend" / "dist"

DJANGO_VITE = {
  "default": {
    "dev_mode": config("DJANGO_VITE_DEV_MODE", default=True, cast=bool),
    "manifest_path": DJANGO_VITE_ASSETS_PATH / '.vite' / 'manifest.json'
  }
}

# Name of static files folder (after called python manage.py collectstatic)
STATIC_ROOT = PROJECT_DIR / "collectedstatic"

# Include DJANGO_VITE_ASSETS_PATH into STATICFILES_DIRS to be copied inside
# when run command python manage.py collectstatic
STATICFILES_DIRS = [DJANGO_VITE_ASSETS_PATH]

REDIS_HOST = config('REDIS_HOST', cast = str, default = 'cmj4redis')
REDIS_PORT = config('REDIS_PORT', cast=int, default=6379)
if DEBUG:
    if FOLDER_DEBUG_CONTAINER != PROJECT_DIR:
        REDIS_HOST = 'localhost'

CELERY_BROKER_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


CACHES = {
    #'default': {
    #    'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #    'LOCATION': '/var/tmp/django_cache',
    #}
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache' if not DEBUG else 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'unique-snowflake',
    }
    #"default": {
    #    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    #    "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
    #}
}
