import os
import south
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings") 

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'v1%#$8(d!6o)o1q8yk1e3v=+*q*!)qzf09=n0zy&f3ihv647q%'
SOUTH_TESTS_MIGRATE = False


DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True
ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'south',
    'pyta',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pyta.middleware.RequestStorage',
)

LOGIN_REDIRECT_URL = '/'
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)


TEMPLATE_CONTEXT_PROCESSORS += (
    'pyta.context_processors.settings_context',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
STATICFILES_DIRS = ( os.path.join(BASE_DIR,'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATE_DIRS = (
    'templates/',
    'pyta/templates/pyta/'
)


ROOT_URLCONF = 'cups42.urls'


WSGI_APPLICATION = 'cups42.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.pyta'),
    }
}


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True



MEDIA_URL = '/media/'
MEDIA_ROOT =  'media/'

