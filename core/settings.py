import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------------------
# SECURITY SETTINGS
# ------------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-3ko70zjdv!v7+5ailo=3rfcx_b0xv$nz60xkg=k69c=hbp2w1z"
)
DEBUG = os.environ.get("DEBUG", "True") == "True"
# DEBUG = False
ALLOWED_HOSTS = ["*"]

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "app",

    # Cloudinary (for image uploads)
    "cloudinary",
    "cloudinary_storage",
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # ✅ For Railway static hosting
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middleware.NoCacheMiddleware",
]

ROOT_URLCONF = "core.urls"

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ------------------------------------------------------------------------------
# DATABASE CONFIGURATION (PostgreSQL on Railway, Local fallback)
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mth',
        'USER': 'postgres',
        'PASSWORD': 'tejas',
        'HOST': 'localhost',  # or IP address
        'PORT': '5432',       # default PostgreSQL port
    }
}

# ------------------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC & MEDIA FILES (Whitenoise + Cloudinary)
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ✅ Cloudinary setup (for production)
if os.environ.get("CLOUDINARY_CLOUD_NAME"):
    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
    CLOUDINARY_STORAGE = {
        "CLOUD_NAME": os.environ.get("Root"),
        "API_KEY": os.environ.get("817363994834176"),
        "API_SECRET": os.environ.get("9cQUgkkNSdgbL5AYLYrdTR120BU"),
    }
else:
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# ------------------------------------------------------------------------------
# DEFAULT SETTINGS
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "app.CustomUser"

# ------------------------------------------------------------------------------
# LOGIN & SESSION MANAGEMENT
# ------------------------------------------------------------------------------
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800  # 30 mins
SESSION_SAVE_EVERY_REQUEST = True

# ------------------------------------------------------------------------------
# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "newmahavirtent@gmail.com"
EMAIL_HOST_PASSWORD = "xnpv yhyc mjfv rkvt"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER




