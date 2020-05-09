import contextlib
import os

import dj_database_url
from dotenv import load_dotenv

with contextlib.suppress(Exception):
	load_dotenv()

# Core Settings
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sorobrain.settings')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ROOT_URLCONF = 'sorobrain.urls'
WSGI_APPLICATION = 'sorobrain.wsgi.application'

SECRET_KEY = os.environ.get('SECRET_KEY')

ADMINS = [
	('Ishan Manchanda', 'ishanmanchanda70@gmail.com'),  # TODO
]

AUTH_USER_MODEL = 'main.User'

# Security Settings
DEBUG = True if os.environ.get('DEBUG', '0') == '1' else False

ALLOWED_HOSTS = ['*']
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SECURE_CONTENT_TYPE_NOSNIFF = \
	SECURE_HSTS_INCLUDE_SUBDOMAINS = \
	SECURE_HSTS_PRELOAD = \
	SECURE_BROWSER_XSS_FILTER = \
	SECURE_SSL_REDIRECT = \
	SESSION_COOKIE_SECURE = \
	CSRF_COOKIE_SECURE = not DEBUG

if not DEBUG:
	X_FRAME_OPTIONS = 'DENY'
	SECURE_REFERRER_POLICY = 'same-origin'
	SECURE_HSTS_SECONDS = 31536000
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database Settings
DATABASES = {
	'default': dj_database_url.config(
		conn_max_age=600,
		default=os.environ.get('DATABASE_URL')
	)
}

# AWS Settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
	'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_DEFAULT_ACL = None

# Static files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'static')]

if DEBUG:
	STATIC_URL = '/static/'
	STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
	WHITENOISE_MAX_AGE = 31536000  # Cache static files for one year
else:
	STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
	STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Media File Storage
DEFAULT_FILE_STORAGE = 'sorobrain.media_storages.MediaStorage'
PRIVATE_FILE_STORAGE = 'sorobrain.media_storages.PrivateMediaStorage'

# Internalization Settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Email Settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'tprocessors@gmail.com'  # TODO
EMAIL_HOST_PASSWORD = os.environ.get('MAILER_PASSWORD')
EMAIL_PORT = 587

# Allauth settings
SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'  # Either can be used to login
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http' if DEBUG else 'https'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Sorobrain]'  # TODO
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# TODO: Forms to override
ACCOUNT_FORMS = {
	'login': 'allauth.account.forms.LoginForm',
	'signup': 'allauth.account.forms.SignupForm',
	# 'add_email': 'allauth.account.forms.AddEmailForm',
	# 'change_password': 'allauth.account.forms.ChangePasswordForm',
	# 'set_password': 'allauth.account.forms.SetPasswordForm',
	# 'reset_password': 'allauth.account.forms.ResetPasswordForm',
	# 'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
	# 'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
}

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
	'google': {
		'APP': {
			'client_id': os.environ.get('OAUTH_GOOGLE_CLIENT_ID'),
			'secret': os.environ.get('OAUTH_GOOGLE_CLIENT_SECRET'),
		},
		'SCOPE': [
			'profile',
			'email',
			'openid',
		],
		'AUTH_PARAMS': {
			'access_type': 'online',

		},
	},
}

# Applications and middleware
INSTALLED_APPS = [
	'whitenoise.runserver_nostatic',  # Needs to be first

	# Django apps
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	# Allauth apps

	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.google',
	# 'allauth.socialaccount.providers.facebook',
	# 'allauth.socialaccount.providers.microsoft',
	# 'allauth.socialaccount.providers.twitter',

	# Installed Apps
	'storages',

	# Custom apps
	'main.apps.MainConfig',
	# TODO: Add other apps
]

if DEBUG:
	INSTALLED_APPS += [
		'django_extensions',
	]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [os.path.join(BASE_DIR, 'templates')],
		'APP_DIRS': True,
		'OPTIONS': {
			# TODO: Look into django.template.loaders.cached.Loader
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.template.context_processors.csrf',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
			'debug': DEBUG,
		},
	},
]

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_PASSWORD_VALIDATORS = [
	{'NAME':
		'django.contrib.auth.password_validation'
		'.UserAttributeSimilarityValidator'},
	{'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
	{'NAME':
		'django.contrib.auth.password_validation.CommonPasswordValidator'},
	{'NAME':
		'django.contrib.auth.password_validation.NumericPasswordValidator'}
]
