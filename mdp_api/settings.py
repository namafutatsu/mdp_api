import os
import dj_database_url

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'prod')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

if ENVIRONMENT == 'dev':
    SECRET_KEY = 'dev-secret-key'
else:
    SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = ENVIRONMENT == 'dev'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

PROJECT_HRID = 'backent'

AUTH_USER_MODEL = 'backent.User'

ROOT_URLCONF = 'backent.urls'

WSGI_APPLICATION = 'backent.wsgi.application'

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

INSTALLED_APPS = [
    'backent',
    'backent.apps.BackentAdminConfig',
    'backent.api',

    'corsheaders',
    'django_countries',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'mapwidgets',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if ENVIRONMENT == 'dev':
    INSTALLED_APPS += [
        'debug_toolbar'
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]
    INTERNAL_IPS = [
        '127.0.0.1',
    ]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': PROJECT_HRID,
    }
}
db_from_env = dj_database_url.config(conn_max_age=500)
db_from_env.pop('ENGINE', None)  # ensure we keep using postgis
DATABASES['default'].update(db_from_env)

if ENVIRONMENT == 'dev':
    CORS_ORIGIN_ALLOW_ALL = True
    ALLOWED_HOSTS = ['*']
else:
    CORS_ORIGIN_ALLOW_ALL = os.environ.get('CORS_ORIGIN_ALLOW_ALL', 'False') == 'True'
    CORS_ORIGIN_WHITELIST = os.environ.get('CORS_ORIGIN_WHITELIST', '').split(',')
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

GOOGLE_RECAPTCHA_SECRET_KEY = os.environ.get('GOOGLE_RECAPTCHA_SECRET_KEY', None)
HAS_RECAPTCHA = ENVIRONMENT != 'dev' and GOOGLE_RECAPTCHA_SECRET_KEY is not None

GOOGLE_MAPS_JAVASCRIPT_API_KEY = os.environ.get('GOOGLE_MAPS_JAVASCRIPT_API_KEY', None)

MAP_WIDGETS = {
    'GOOGLE_MAP_API_KEY': GOOGLE_MAPS_JAVASCRIPT_API_KEY,
    'LANGUAGE': 'fr',
    'GooglePointFieldWidget': (
        ('zoom', 14),
        ('mapCenterLocationName', 'paris'),
        ('markerFitZoom', 12),
    ),
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

API_EVENT_LIST_CACHE_DURATION = int(os.environ.get('API_EVENT_LIST_CACHE_DURATION', 60 * 60 * 24))
