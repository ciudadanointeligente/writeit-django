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

INSTALLED_APPS = (
    'south',
    'writeit',
    'popit',
    # Uncomment the next line to enable the admin:
    'django_nose',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

#setting to avoid db changes during test
SOUTH_TESTS_MIGRATE = False

TEST_POPIT_API_URL = 'http://popit.mysociety.org'
WRITEIT_USERNAME = 'admin'
WRITEIT_KEY = 'e8e11c885307d4709ce64365a5d54acf2a8e11fc'
