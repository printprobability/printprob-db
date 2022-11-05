import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ["DEBUG_STATUS"] == "True"

ALLOWED_HOSTS = [os.environ["ALLOWED_HOSTS"], f"{os.environ['ALLOWED_HOSTS']}:8080"]

IMAGE_BASEURL = os.environ["IMAGE_BASEURL"]
REAL_IMAGE_BASEDIR = "/vol/img"

# Application definition

INSTALLED_APPS = [
    "pp.apps.ppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "rest_framework",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "drf_yasg",
    "rest_framework.authtoken",
    "django_filters",
    "drf_tweaks",
    # "silk",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "silk.middleware.SilkyMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [f"http://{ah}" for ah in ALLOWED_HOSTS]
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = "xsrfcookie"
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

ROOT_URLCONF = "web.urls"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "web.wsgi.application"

SILKY_AUTHENTICATION = True

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissions",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "HTML_SELECT_CUTOFF": 10,
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Token-based authentication.  The key should be prefixed by the string literal 'Token', with whitespace separating the two strings. For example: `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`",
        }
    }
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
        "CONN_MAX_AGE": 600, # 10 minutes
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.environ["STATIC_ROOT"]
CA_CERT_ROUTE = os.environ["CA_CERT_ROUTE"]
if (
    CA_CERT_ROUTE == "False"
):  # If we want to skip verification, e.g. during testing, passing false needs to convert this setting into a boolean FALSE instead
    CA_CERT_ROUTE = False
DOWNLOAD_SCRATCH_DIR = os.environ["DOWNLOAD_SCRATCH_DIR"]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 25)
DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_ADDRESS")

# Allow large data file
DATA_UPLOAD_MAX_MEMORY_SIZE = 3000000000

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Django Logging Information
# LOGGING = {
#     # Define the logging version
#     'version': 1,
#     # Enable the existing loggers
#     'disable_existing_loggers': False,
#
#     # Define the handlers
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'djangoapp.log',
#         },
#
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#
#     # Define the loggers
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#
#         },
#     },
# }