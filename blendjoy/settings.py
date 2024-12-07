"""
Django settings for blendjoy project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
import environ
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


GOOGLE_OAUTH_CLIENT_ID = env("GOOGLE_OAUTH_CLIENT_ID")
if not GOOGLE_OAUTH_CLIENT_ID:
    raise ValueError(
        "GOOGLE_OAUTH_CLIENT_ID is missing." "Have you put it in a file at core/.env ?"
    )

# We need these lines below to allow the Google sign in popup to work.
SECURE_REFERRER_POLICY = "no-referrer-when-downgrade"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ws&oot&xi!ow-u*z^41i-+2r5_wl$@+khj6oa*&8!praes6f7f"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "crispy_forms",
    "crispy_tailwind",
    "loginas",
    "channels",
    "pwa",
    "app",
    "django_celery_results",
    "app.authentication",
    "app.books",
    "app.websockets",
    "app.forum",
    "app.social_newsfeed",
    "app.rewards",
    "app.notifications",
    "app.chat",
]

CSRF_TRUSTED_ORIGINS = ["https://readify-dev.up.railway.app", "http://localhost:8000", "https://readify.blog"]

# CSRF_COOKIE_DOMAIN = "up.railway.app"

CSRF_COOKIE_SECURE = True

CORS_ORIGIN_WHITELIST = ["https://readify-dev.up.railway.app", "http://localhost:8000", "https://readify.blog"]

# Setup support for proxy headers
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blendjoy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ASGI config
ASGI_APPLICATION = "blendjoy.asgi.application"
WSGI_APPLICATION = "blendjoy.wsgi.application"


CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env("POSTGRES_DB"),
#         "USER": env("POSTGRES_USER"),
#         "PASSWORD": env("POSTGRES_PASSWORD"),
#         "HOST": env("POSTGRES_HOST"),
#         "PORT": env("POSTGRES_PORT"),
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# This production code might break development mode, so we check whether we're in DEBUG mode
if not DEBUG:
    # Tell Django to copy static assets into a path called `staticfiles` (this is specific to Render)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Enable the WhiteNoise storage backend, which compresses static files to reduce disk use
    # and renames the files with unique names for each version to support long-term caching
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "authentication.User"


LOGIN_REDIRECT_URL = "/home"
LOGOUT_REDIRECT_URL = "/signin"

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

UNFOLD = {
    "SITE_TITLE": "Readify Admin",
    "SITE_HEADER": "Readify Admin",
    "css": [
        "static/css/admin.css",  # path to your custom CSS file
    ],
    "SIDEBAR": {
        "show_search": True,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": "Analytics",
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "bar_chart_4_bars",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:custom_name"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Authentication",
                "items": [
                    {
                        "title": "User",
                        "icon": "manage_accounts",
                        "link": reverse_lazy("admin:authentication_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Books",
                "items": [
                    {
                        "title": "Book Libraries",
                        "icon": "library_books",
                        "link": reverse_lazy("admin:books_books_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:books_categories_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Chapter Unlocked By User",
                        "icon": "lock_open_right",
                        "link": reverse_lazy(
                            "admin:books_chapterunlockedbyuser_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Chapters per book",
                        "icon": "auto_stories",
                        "link": reverse_lazy("admin:books_bookschapter_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Plagiarism Checker Logs",
                        "icon": "plagiarism",
                        "link": reverse_lazy(
                            "admin:books_plagiarismcheckerlogs_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Chat",
                "items": [
                    {
                        "title": "Messages",
                        "icon": "chat",
                        "link": reverse_lazy("admin:chat_message_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Forum",
                "items": [
                    {
                        "title": "Communities",
                        "icon": "communities",
                        "link": reverse_lazy("admin:forum_community_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Communities Members",
                        "icon": "groups",
                        "link": reverse_lazy("admin:forum_communitymembers_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Topics",
                        "icon": "topic",
                        "link": reverse_lazy("admin:forum_topic_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Topics Comment Replies",
                        "icon": "reply",
                        "link": reverse_lazy(
                            "admin:forum_topiccommentreply_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": "Topics Comments",
                        "icon": "comment",
                        "link": reverse_lazy("admin:forum_topiccomments_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Rewards",
                "items": [
                    {
                        "title": "User's Rewards",
                        "icon": "rewarded_ads",
                        "link": reverse_lazy("admin:rewards_rewards_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": "Social Newsfeed",
                "items": [
                    {
                        "title": "Posts",
                        "icon": "post",
                        "link": reverse_lazy(
                            "admin:social_newsfeed_socialpost_changelist"
                        ),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
        ],
    },
}

SENDGRID_RECOVERY_CODE = "7VW6TVXK9PQQ4F199J4DKB82"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "kaleigh1201@gmail.com"
EMAIL_HOST_PASSWORD = "xiqs ktll rher tfjo"

"fmwn zssh hvmw wbeh"

CELERY_BROKER_URL = env("CELERY_BROKER_URL_REDIS")
CELERY_RESULT_BACKEND = env("CELERY_BROKER_URL_REDIS")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
# CELERY_BEAT_SCHEDULE = {
#     "run_my_task": {
#         "task": "apps.tasks.get_instagram_post",  # Replace 'yourapp' with your app name
#         "schedule": 3600,  # Run every 60 seconds
#         # 'schedule': crontab(hour=0, minute=1),  # Schedule it to run every day at 12:01 AM
#     },
# }
# CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_RESULT_EXTENDED = True

"""
celery -A blendjoy worker --loglevel=info --pool=eventlet
celery -A blendjoy beat --loglevel=info
"""


PWA_APP_NAME = "Readify"
PWA_APP_DESCRIPTION = "Better way to read your friction textbooks"
PWA_APP_THEME_COLOR = "#ec4899"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "portrait"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [{"src": "/static/images/icon512_rounded.png", "sizes": "160x160"}]
PWA_APP_ICONS_APPLE = [
    {"src": "/static/images/icon512_rounded.png", "sizes": "160x160"}
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "/static/images/icon512_rounded.png",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-US"
# PWA_APP_SHORTCUTS = [
#     {
#         "name": "Shortcut",
#         "url": "/target",
#         "description": "Shortcut to a page in my application",
#     }
# ]
PWA_APP_SCREENSHOTS = [
    {
        "src": "/static/images/icon512_rounded.png",
        "sizes": "750x1334",
        "type": "image/png",
    }
]
PWA_APP_DEBUG_MODE = False