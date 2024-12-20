from pathlib import Path
from decouple import AutoConfig
from dj_database_url import parse as db_url
#from .apps import *
#from .auth import *
#from .drf import *
#from .email import *
#from .frontend import *
#from .languages import *
#from .logs import *
#from .medias import *
#from .middleware import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent.parent
PROJECT_DIR = BASE_DIR.parent

config = AutoConfig(search_path=BASE_DIR)

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=True, cast=bool)

FOLDER_DEBUG_CONTAINER = Path(config('FOLDER_DEBUG_CONTAINER', default=__file__, cast=str))

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'daphne',
    'channels',

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

    'haystack',
    'celery_haystack',

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATABASES = {
    'default': config(
        'DATABASE_URL_DEV' if DEBUG else 'DATABASE_URL_PRD',
        cast=db_url,
    )
}

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

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

DJANGO_VITE_ASSETS_PATH = PROJECT_DIR / "_frontend" / "dist"
DJANGO_VITE_DEV_MODE = config("DJANGO_VITE_DEV_MODE", default=True, cast=bool)
DJANGO_VITE_DEV_MODE = DJANGO_VITE_DEV_MODE and DEBUG
DJANGO_VITE = {
  "default": {
    "dev_mode": DJANGO_VITE_DEV_MODE,
    "manifest_path": DJANGO_VITE_ASSETS_PATH / '.vite' / 'manifest.json'
  }
}

# Name of static files folder (after called python manage.py collectstatic)
STATIC_URL = "/static/"
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

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}

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

USE_SOLR = True
SOLR_URL = 'http://solr:solr@cmjsolr:8983'
HAYSTACK_SIGNAL_PROCESSOR = 'cmj4.haystack.CelerySignalProcessor'

if DEBUG:
    if FOLDER_DEBUG_CONTAINER != PROJECT_DIR:
        # HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
        SOLR_URL = 'http://solr:solr@localhost:8983'
        REDIS_HOST = 'localhost'

SOLR_COLLECTION = 'portalcmj4_cmj'

SEARCH_BACKEND = 'haystack.backends.solr_backend.SolrEngine'
SEARCH_URL = ('URL', '{}/solr/{}'.format(SOLR_URL, SOLR_COLLECTION))
HAYSTACK_ROUTERS = ['cmj4.haystack.CmjDefaultRouter']
HAYSTACK_ITERATOR_LOAD_PER_QUERY = 100
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': SEARCH_BACKEND,
        SEARCH_URL[0]: SEARCH_URL[1],
        'BATCH_SIZE': 1000,
        'TIMEOUT': 600,
        'EXCLUDED_INDEXES': [
            # 'cmj.arq.search_indexes.ArqDocIndex',
        ]
    },
    'cmjarq': {
        'ENGINE': SEARCH_BACKEND,
        'URL': '{}/solr/{}'.format(SOLR_URL, 'portalcmj4_arq'),
        'BATCH_SIZE': 1000,
        'TIMEOUT': 600,
        'EXCLUDED_INDEXES': [
            # 'cmj.search.search_indexes.DiarioOficialIndex',
            # 'cmj.search.search_indexes.NormaJuridicaIndex',
            # 'cmj.search.search_indexes.DocumentoAcessorioIndex',
            # 'cmj.search.search_indexes.MateriaLegislativaIndex',
            # 'cmj.search.search_indexes.SessaoPlenariaIndex',
            # 'cmj.search.search_indexes.DocumentoAdministrativoIndex',
            # 'cmj.search.search_indexes.DocumentoIndex',
        ]
    },
}

