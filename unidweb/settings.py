"""
Django settings for unidweb project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import pymysql

pymysql.install_as_MySQLdb()


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8ev70!908of3wx4w-n85a6v&p55c(f+6uew=&pvf@kc&g+@a=&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'unid',
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'haystack',
    #
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # # ... include the providers you want to enable:
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.facebook',
    
]

CRONJOBS = [
    ('0 0 * * *', 'unid.views.my_cron_job'),
    ('50 1 * * *', 'unid.views.writer_rewards'),
    ('50 1 * * *', 'unid.views.liked_users_reward'),
    ('30 23 * * *', 'unid.views.checkCrowd')
]


WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh_index')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    },

    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ROOT_URLCONF = 'unidweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                'django.template.context_processors.request',
            ],
        },
    },
]

# -----------oauth------------------------------------------
AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)
# -----------oauth------------------------------------------
SITE_ID = 7  # 안맞으면 site maching the query ... 이거 대체 뭘까
LOGIN_URL = '/unid/login/'
LOGIN_REDIRECT_URL = '/unid/createaccount/'
ACCOUNT_LOGOUT_REDIRECT_URL = "/unid"
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
WSGI_APPLICATION = 'unidweb.wsgi.application'

SOCIALACCOUNT_ADAPTER = 'unid.my_adapter.MyAdapter'

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

AUTH_USER_MODEL = 'auth.User'
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
   'default': {
       # 'ENGINE': 'django.db.backends.sqlite3',
       # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),


       'ENGINE': 'django.db.backends.mysql',
       'OPTIONS': {
           'read_default_file': './db/cnf',
           'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
           # 'charset': 'utf8'
           },
       'NAME': 'unid_db',  #mysql
       'USER': 'unid', #root
       'PASSWORD': 'qhdkscjfwj0!', #1234
       'HOST': '222.239.231.251', #공백으로 냅두면 default localhost
       'PORT': '3306' #공백으로 냅두면 default 3306
       # 'NAME': 'unid_db',  # mysql
       # 'USER': 'jun',  # root
       # 'PASSWORD': 'jun',  # 1234
       # 'HOST': '210.107.78.157',  # 공백으로 냅두면 default localhost
       # 'PORT': '3306'  # 공백으로 냅두면 default 3306
   }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 실제 파일이 위치하는 서버상 경로
MEDIA_URL = '/media/' # MEDIA 파일이 접근하는 URL이 저거로 시작
