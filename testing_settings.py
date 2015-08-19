# Django settings for writeit project.
import sys
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'writeit-django.db',                      # Or path to database file if using sqlite3.
    }
}


gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    ('es', gettext('Spanish'))
    )

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True
# Make this unique, and don't share it with anybody.
SECRET_KEY = 'Soy la fiera y vengo a ladrar'

# List of callables that know how to import templates from various sources.

ROOT_URLCONF = 'writeit.tests.urls'

# Python dotted path to the WSGI application used by Django's runserver.

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
TESTING = 'test' in sys.argv

STATIC_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    # 'south',
    'writeit',
    # 'popit',
    'popolo',
    # Uncomment the next line to enable the admin:
    'django_nose',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'rest_framework',
    'popolorest',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

#I lauched this one in start_writeit_for_testing.bash
LOCAL_TESTING_WRITEIT = 'http://127.0.0.1.xip.io:3001/api/v1'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#setting to avoid db changes during test
SOUTH_TESTS_MIGRATE = False

TEST_POPIT_API_URL = 'http://localhost:3000'

#check from line 4 to 19 in example_data.yaml
WRITEIT_USERNAME = 'admin'
WRITEIT_KEY = 'a'

# POPIT TESTING RELATED
TEST_POPIT_API_HOST_IP   = '127.0.0.1'
TEST_POPIT_API_PORT      = '3000'
TEST_POPIT_API_SUBDOMAIN = 'popit-django-test'

# We have our local popit instance for testing porpouses running using 
# the bash file start_local_popit_api.bash
# create the url to use for testing the database.
# See http://xip.io/ for details on the domain used.
TEST_POPIT_API_URL = "http://%s.%s.xip.io:%s/api" % ( TEST_POPIT_API_SUBDOMAIN,
                                                      TEST_POPIT_API_HOST_IP,
                                                      TEST_POPIT_API_PORT )
