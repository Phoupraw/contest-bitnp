"""Django settings for contest project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from __future__ import annotations

from os import environ, getenv
from pathlib import Path
from shutil import which

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if getenv("DJANGO_PRODUCTION"):
    SECRET_KEY = environ["SECRET_KEY"]
else:
    SECRET_KEY = getenv(
        "SECRET_KEY",
        default="django-insecure-$cwq@cw1*q!9490s%a-%b=#vf*l(hhed$swpy5eu#f0&ahx=v4",
    )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not bool(getenv("DJANGO_PRODUCTION"))


def _debug_only(*args) -> tuple:
    """只在`DEBUG`下启用

    Examples
    --------
    ```
    SOME_CONFIG = [
        "pre",
        *_debug_only("dev"),
        "post",
    ]
    ```

    `DEBUG`下`SOME_CONFIG`是`["pre", "dev", "post"]`，否则是`["pre", "post"]`。
    """
    if DEBUG:
        return args
    else:
        return ()


ALLOWED_HOSTS: list[str] = [
    ".localhost",
    "127.0.0.1",
    "[::1]",
    "contest.bitnp.net",  # production
    "contest-test.bitnp.net",  # for deployment test
    "everything411.top",
]
# 这是 DEBUG 下的默认


# Application definition

INSTALLED_APPS = [
    "quiz.apps.QuizConfig",
    "quiz.templatetags",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cas_ng",
    "tailwind",  # 因为含模板 tag，即使无需构建前端也必要
    "theme",  # todo: 提供 static，由 Django 负责静态文件时需要
    "js",  # todo: 同 theme
    *_debug_only("django_browser_reload"),
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    *_debug_only("django_browser_reload.middleware.BrowserReloadMiddleware"),
    "django_cas_ng.middleware.CASMiddleware",
]

ROOT_URLCONF = "contest.urls"

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
            ],
            "debug": DEBUG,  # for django_coverage_plugin
        },
    },
]

WSGI_APPLICATION = "contest.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom Django auth settings

AUTH_USER_MODEL = "quiz.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "quiz:index"

# CAS server
# https://docs.djangoproject.com/zh-hans/4.2/ref/settings/#authentication-backends
# https://djangocas.dev/blog/django-cas-ng-example-project/
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "quiz.auth_backends.CASBackend",
]
CAS_SERVER_URL = "https://login.bit.edu.cn/devcas/"
CAS_LOGIN_URL_NAME = LOGIN_URL
CAS_LOGOUT_URL_NAME = "logout"  # 会用于 Django 提供的模板，如 admin
CAS_REDIRECT_URL = LOGIN_REDIRECT_URL
CAS_CHECK_NEXT = False

CSRF_TRUSTED_ORIGINS = [
    "https://contest.bitnp.net",
    "https://contest-test.bitnp.net",
    "https://everything411.top",
]

# Tailwind
# https://django-tailwind.readthedocs.io/en/latest/installation.html

if DEBUG:
    TAILWIND_APP_NAME = "theme"
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

    # `just manage tailwind install`需要 Node.js
    NPM_BIN_PATH = which("pnpm")
    # Windows 有`$PATHEXT`问题，而`subprocess.run()`应尽量保证是完成路径。
    # https://github.com/timonweb/django-tailwind/pull/181
