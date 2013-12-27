# Global settings for {{ project_name }} project.
import os
import sys

PROJECT_PATH_INNER = os.path.dirname(__file__)
PROJECT_PATH = os.path.dirname(PROJECT_PATH_INNER)
APPLIB_DIR = os.path.join(PROJECT_PATH, "applib")

if APPLIB_DIR not in sys.path[:2]:
  sys.path.insert(1, APPLIB_DIR)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Make this unique, and don't share it with anybody.
SECRET_KEY = r"{{ secret_key }}"

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'assets/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'assets/static-destination')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'assets/assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',    
)

ROOT_URLCONF = '{{ project_name }}.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, '{{ project_name }}/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    
    '{{ project_name }}.misc.context_processors.date_formats',
    '{{ project_name }}.misc.context_processors.serve_media_locally',
    
    #AllAuth
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',    
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

FIXTURE_DIRS = (
    os.path.join(PROJECT_PATH, 'fixtures'),
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

########## APP CONFIGURATION
INSTALLED_APPS = (
    ##### DJANGO_APPS #####
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    'django.contrib.admindocs',

    
    ##### THIRD_PARTY_APPS #####
    # System/pip installed 3rd party apps
    'south',
    'gunicorn',
    'storages',
    's3_folder_storage',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.twitter',
    
    
    ##### APPLIB_APPS #####
    # 3rd party apps that have been modified and placed in /applib
    # /applib is added to path
    
    #'moded_third_party_app',


    ##### PROJECT_APPS #####
    # Project apps - utility
    '{{ project_name }}.misc',      #gets views and urls, incl basic homepage
    '{{ project_name }}.templates', #gets template tags
    
    # Project apps - core
    #'{{ project_name}}.myapp',

)    
########## END APP CONFIGURATION


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#AllAuth Settings
# See: http://django-allauth.readthedocs.org/en/latest/
ACCOUNT_AUTHENTICATION_METHOD = "username" 
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[{{ project_name }}]"

#Set this
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# Until 1.7 it is probably a good idea to set it like this
# ALLOWED_HOSTS = [
#    '.{{ project_name }}.com', # Allow domain and subdomains
#    '.{{ project_name }}.com.', # Also allow FQDN and subdomains
# ]
ALLOWED_HOSTS = ["*"]

#######################################
#ENVIRONMENTS
####################################### 
# Manage environment specific settings with DJANGO_ENV 
# variable and an if-else switch. Unlike separate 
# settings files for each environment, this keeps all 
# settings in one place. 
#
# Keep secrets and passwords safe by storing them in 
# environment variables and outside of the repo. 
#
# Most environment variables are not given fallbacks
# Better to fail early and informatively than to 
# initially appear to work and later fail obscurely
#
# DJANGO_ENV retrieval failures made verbose and informative
#######################################
CONFIGURED_ENVIRONMENTS = "Default DJANGO_ENV choices: 'PRODUCTION', 'TEST', 'DEV'"
assert 'DJANGO_ENV' in os.environ, 'Set DJANGO_ENV environment variable! %s' % CONFIGURED_ENVIRONMENTS
DJANGO_ENV = os.environ.get('DJANGO_ENV', None)
assert DJANGO_ENV in ["PRODUCTION", "TEST", "DEV"], "DJANGO_ENV set to '%s'.  %s" % (DJANGO_ENV, CONFIGURED_ENVIRONMENTS)


####################################### 
#PRODUCTION ENVIRONMENT
####################################### 
if DJANGO_ENV == "PRODUCTION":
  #BEHAVIOR FLAGS
  # To make it easier to turn DEBUG on and off
  # heroku config:add DJANGO_DEBUG=true
  # heroku config:add DJANGO_DEBUG=false
  DEBUG = os.environ.get('DJANGO_DEBUG', 'false').lower() == 'true'
  TEMPLATE_DEBUG = DEBUG
  SERVE_MEDIA_LOCALLY = False
  
  #DATABASE
  import dj_database_url  
  DATABASES = {'default': dj_database_url.config(default='postgres://localhost/{{ project_name }}')}  
  
  #EMAIL
  EMAIL_HOST= 'smtp.sendgrid.net'
  EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
  EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True

  #AWS KEYS
  AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
  AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
  AWS_STORAGE_BUCKET_NAME = '{{project_name}}-assets-production'

  #ASSETS: STATIC FILES, MEDIA
  DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
  STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
  DEFAULT_S3_PATH = "media"
  STATIC_S3_PATH = "static"

  MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
  STATIC_ROOT = "/%s/" % STATIC_S3_PATH
  MEDIA_URL = 'http://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
  STATIC_URL = 'http://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
  ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
  
  #CACHES
  #QUEUES
  #MONITORING

  #ENVIRONMENT APP ADDITIONS
  INSTALLED_APPS += (
    
  )

  #ENVIRONMENT MIDDLEWARE ADDITIONS
  MIDDLEWARE_CLASSES += (
    
  )
  
  #Warn of overly permissive default ALLOWED_HOSTS setting.
  if ALLOWED_HOSTS == ["*"]:
    raise ValueError("setttings.ALLOWED_HOSTS is set to '*', update this to an appropriate value.  This error will only show in DEV")
  
########## END PRODUCTION ENVIRONMENT SETTINGS



####################################### 
# TESTING ENVIRONMENT  
#######################################
elif DJANGO_ENV == "TEST":
  # Not set up by default
  # should be exact settings as production with different servers/databases
  raise NotImplementedError("TEST environment settings have not been set up")
########## END TESTING ENVIRONMENT SETTINGS


    
#######################################   
# DEV ENVIRONMENT SETTINGS
####################################### 
elif DJANGO_ENV == "DEV":
  #BEHAVIOR FLAGS
  # To make it easier to turn DEBUG on and off
  DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() == 'true'
  TEMPLATE_DEBUG = DEBUG
  SERVE_MEDIA_LOCALLY = True
  
  #DATABASE
  import dj_database_url
  DATABASES = {'default': dj_database_url.config(default='postgres://user:pass@localhost/{{project_name}}')}
  # Alt database settings
  # DATABASES = {
  #   'default': {
  #     'ENGINE': 'django.db.backends.sqlite3',
  #     'NAME': '{{ project_name }}.db',
  #     'USER': '',
  #     'PASSWORD': '',
  #     'HOST': '',
  #     'PORT': '',
  #   }
  # }
    
  #EMAIL
  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

  #ASSETS: STATIC FILES, MEDIA
  MEDIA_URL = '/media/'
  STATIC_URL = '/static/'  

  #CACHES
  #QUEUES
  #MONITORING
    
  #ENVIRONMENT APP ADDITIONS
  INSTALLED_APPS += (
    'functests',
    'debug_toolbar',
  )

  #ENVIRONMENT MIDDLEWARE ADDITIONS
  MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
  )
  
  #DEBUG TOOLBAR SETTINGS
  INTERNAL_IPS = ('127.0.0.1',)
  # custom_show_toolbar shows toolbar for superusers
  def custom_show_toolbar(request): return request.user.is_superuser
  DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
  }

  # LOCAL SETTINGS
  # Tolerate local settings in DEV environment 
  try:
      LOCAL_SETTINGS
  except NameError:
      try:
          from local_settings import *
      except ImportError:
          pass
########## END DEV ENVIRONMENT SETTINGS

          