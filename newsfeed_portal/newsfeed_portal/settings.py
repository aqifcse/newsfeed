import os
import mimetypes
from pathlib import Path
from decouple import config

mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ")&e(_=tu8d_r&&8r4=^3il%%n42^42n5k%5@wte)wldj4dx(xh"

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "portal",  # App
    "corsheaders",  # For future JS Frontend
    "crispy_forms",  # For crispy forms
    "rest_framework",  # For REST API
    "django_json_widget",  # For json editor in admin
    "whitenoise",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ]
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # for cors
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "newsfeed_portal.middleware.open_access_middleware",  # for cors
]

# For future JS Fronend, we need corsheaders and whitelist for backend frontend communication
# Future frontend will access whitelist addresses
CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:8000", "https://newsapi.org"]

CORS_ALLOWED_ALL_ORIGINS = True

CRISPY_TEMPLATE_PACK = "bootstrap4"

ROOT_URLCONF = "newsfeed_portal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "newsfeed_portal.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Stockholm"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "portal.User"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "email-smtp.ap-southeast-2.amazonaws.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

# ----------------Sendgrid settings for sending email---------------------------------------------------
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# Toggle sandbox mode (when running in DEBUG mode)
# SENDGRID_SANDBOX_MODE_IN_DEBUG=True

# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
# SENDGRID_ECHO_TO_STDOUT=True
# --------------------Sendgrid Ends----------------------------------------------------------------------

# APIKEY = "cbdd86a002e24e569b7905729d546e91"  # NewsAPI key

APIKEY = "e528c2d1bddb44828d84948700b257c4"
