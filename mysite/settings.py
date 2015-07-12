"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rblp+v-vm(l7&9cwvw3(wyx#jfwuo%n^5*g!h%#+z^q(@omk8%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    #http://django-haystack.readthedocs.org/en/v2.4.0/toc.html
    'haystack',
    #https://github.com/ericflo/django-pagination/blob/master/docs/usage.txt
    'pagination',
    'cardtravel',
    'south',
    #http://django-postman.readthedocs.org/en/latest/index.html
    'postman',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'postman.context_processors.inbox',
)   

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DELETE_MESSAGES = 50

MESSAGE_TAGS = {
    DELETE_MESSAGES: 'deleted',
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(os.path.expanduser('~'), 'projects/django/mysyte/static/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static/'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

DEBUG_TOOLBAR_PATCH_SETTINGS = False

INTERNAL_IPS = '127.0.0.1'

LOGIN_URL = '/login/'

#http://django-haystack.readthedocs.org/en/v2.4.0/tutorial.html
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

#https://github.com/ericflo/django-pagination/blob/master/docs/usage.txt

PAGINATION_DEFAULT_PAGINATION = 6

PAGINATION_DEFAULT_WINDOW = 3

PAGINATION_DEFAULT_ORPHANS = 5

PAGINATION_INVALID_PAGE_RAISES_404 = True

#http://django-postman.readthedocs.org/en/latest/quickstart.html

POSTMAN_DISALLOW_ANONYMOUS = True  # default is False
# POSTMAN_DISALLOW_MULTIRECIPIENTS = True  # default is False
# POSTMAN_DISALLOW_COPIES_ON_REPLY = True  # default is False
# POSTMAN_DISABLE_USER_EMAILING = True  # default is False
POSTMAN_AUTO_MODERATE_AS = True  # default is None
POSTMAN_SHOW_USER_AS = 'get_full_name'  # default is None
POSTMAN_QUICKREPLY_QUOTE_BODY = True  # default is False
# POSTMAN_NOTIFIER_APP = None  # default is 'notification'
# POSTMAN_MAILER_APP = None  # default is 'mailer'
# POSTMAN_AUTOCOMPLETER_APP = {
    # 'name': '',  # default is 'ajax_select'
    # 'field': '',  # default is 'AutoCompleteField'
    # 'arg_name': '',  # default is 'channel'
    # 'arg_default': 'postman_friends',  # no default, mandatory to enable the feature
# }  # default is {}