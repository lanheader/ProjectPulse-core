# -*- coding: UTF-8 -*-

import logging
import os
from datetime import timedelta
from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["*"]),
    SECRET_KEY=(
        str,
        "django-insecure-@1lnlj-tbqnvp5e)&f!q7oqvwyi(%5meql4+0&ddd#(zh493#2",
    ),
    DATABASE_URL=(str, "mysql://root:@127.0.0.1:3306/archery"),
    CACHE_URL=(str, "redis://127.0.0.1:6379/0"),
    # CSRF_TRUSTED_ORIGINS=subdomain.example.com,subdomain.example2.com subdomain.example.com
    CSRF_TRUSTED_ORIGINS=(list, []),
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")
# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")
# 解决nginx部署跳转404
USE_X_FORWARDED_HOST = True
# 请求限制
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
    "apps.apps.AppsConfig",
    "common.apps.CommonConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
]

ROOT_URLCONF = "ProjectPulse.urls"

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

WSGI_APPLICATION = "ProjectPulse.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# 该项目本身的mysql数据库地址
DATABASES = {
    "default": {
        "ENGINE": "dj_db_conn_pool.backends.mysql",
        **env.db(),
        **{
            "DEFAULT_CHARSET": "utf8mb4",
            "CONN_MAX_AGE": 3600,
            "OPTIONS": {
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
                "charset": "utf8mb4",
            },
            "POOL_OPTIONS": {
                "POOL_SIZE": env("DATABASE_POOL_SIZE", default=1),
                "MAX_OVERFLOW": env("DATABASE_MAX_OVERFLOW", default=1),
                "RECYCLE": env("DATABASE_RECYCLE", default=50),
            },
            "TEST": {
                "NAME": "test_archery1",
                "CHARSET": "utf8mb4",
            },
        },
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
        "OPTIONS": {
            "min_length": 9,
        },
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

USE_L10N = True

USE_TZ = False
# Static files (CSS, JavaScript, Images)


# 扩展django admin里users字段用到，指定了sql/models.py里的class users
AUTH_USER_MODEL = "apps.Users"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # 全局配置异常模块
    "DEFAULT_RENDERER_CLASSES": (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 鉴权
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"  # 默认权限为验证用户
    ],
    # 限速（anon：未认证用户  user：认证用户）
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "120/min", "user": "600/min"},
    # 过滤
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    # 分页
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
}

# Swagger UI
SPECTACULAR_SETTINGS = {
    "TITLE": "project API",
    "DESCRIPTION": "OpenAPI 3.0",
    "VERSION": "1.0.0",
}

# JWT配置 https://zhuanlan.zhihu.com/p/633173061
SIMPLE_JWT = {
    "AUTH_HEADER_NAME": 'HTTP_AUTHORIZATION',
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=4),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY
}
