
import os
import environ
from os.path import basename

env = environ.Env()
SETTINGS_DIR = environ.Path(__file__) - 1
DJANGO_ROOT = environ.Path(__file__) - 2
SETTINGS_NAME = basename(str(SETTINGS_DIR))
PROJECT_NAME = basename(str(DJANGO_ROOT))
PROJECT_TEMPLATES = [
    str(DJANGO_ROOT.path('templates')),
]

env_file = str(DJANGO_ROOT.path('security/environ_prod.env'))
environ.Env.read_env(str(env_file))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = env('SECRET_KEY')


DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'api',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = '%s.urls' % SETTINGS_NAME


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': PROJECT_TEMPLATES,
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

WSGI_APPLICATION = '%s.wsgi.application' % SETTINGS_NAME



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


import djcelery
djcelery.setup_loader()

# BROKER_URL = 'amqp://TXltB7ZR:**@scared-strawberry-43.bigwig.lshift.net:10982/dXwsXSuTq6kt'
BROKER_URL = "amqp://guest:guest@localhost:5672//"
BROKER_TRANSPORT = 'amqp'
CELERY_RESULT_BACKEND = "amqp"
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_TASK_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

MONGODB_USER = env('MONGODB_USER')
MONGODB_PASSWD = env('MONGODB_PASSWD')
MONGODB_HOST = env('MONGODB_HOST')
MONGODB_NAME = env('MONGODB_NAME')
MONGODB_DATABASE_HOST = \
    'mongodb://%s:%s@%s/%s' \
    % (MONGODB_USER, MONGODB_PASSWD, MONGODB_HOST, MONGODB_NAME)


STATIC_ROOT = str(DJANGO_ROOT.path('run/static'))
MEDIA_ROOT = str(DJANGO_ROOT.path('run/media'))

STATICFILES_DIRS = [
    str(DJANGO_ROOT.path('static')),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_EXPIRY = 60 * 60 * 24 * 7
AWS_PRELOAD_METADATA = True
AWS_HEADERS = {
    'Cache-Control': u'max-age={0:d}, s-maxage={1:d}, must-revalidate'.format(
        AWS_EXPIRY, AWS_EXPIRY)
}

STATICFILES_LOCATION = 'static'
STATIC_URL = u"https://{0:s}/{1:s}/".format(AWS_S3_CUSTOM_DOMAIN,
                                            STATICFILES_LOCATION)
STATICFILES_STORAGE = 'api.custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = u"https://{0:s}/{1:s}/".format(AWS_S3_CUSTOM_DOMAIN,
                                           MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'api.custom_storages.MediaStorage'