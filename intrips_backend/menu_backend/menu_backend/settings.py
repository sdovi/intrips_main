import os
from pathlib import Path

# ?????????? ??????? ?????????? ???????
BASE_DIR = Path(__file__).resolve().parent.parent

# ????????????
SECRET_KEY = 'django-insecure-)53v0ge)16+9c=q^hq9ky5uhyn96ey_x)3tm(=evp-#(wj#19'
DEBUG = True

ALLOWED_HOSTS = ["intrips.site", "www.intrips.site", "intrips.space", "sanmarin.intrips.site", "www.sanmarin.intrips.site", "127.0.0.1", "shop.intrips.site", "www.shop.intrips.site",
    "localhost",]
CSRF_TRUSTED_ORIGINS = ["https://intrips.site", "https://www.intrips.site"]

# ????????? ??? ???????
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"  # Django ????? ???????? ??????? ????

# ????????? ??? ?????
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ??????????
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    

    'main',
    'rest_framework',
    'chat',
    'django_extensions',
    'custom_admin',
    'corsheaders',
    

]

# ???????????
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'custom_admin.middleware.ConfirmUserMiddleware',





]





ROOT_URLCONF = 'menu_backend.urls'

# ???????
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
                
                "custom_admin.context_processors.new_orders_count",  # ✅ добавляем сюда
            ],
        },
    },
]

# WSGI-??????????
WSGI_APPLICATION = 'menu_backend.wsgi.application'

# ???? ??????
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ??????? ?????? ??????
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "820722zz"
}

# ?????????? ???????
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

CORS_ALLOWED_ORIGINS = [
    "https://shop.intrips.site",
    "https://intrips.space",
    "https://www.intrips.space",
    "https://sanmarin.intrips.site", 
    "https://www.sanmarin.intrips.site",
    
    "http://localhost:3000",  # Добавьте это для локальной разработки
    "http://127.0.0.1:3000",  # Добавьте это для локальной разработки
]

CORS_ALLOW_ALL_ORIGINS = True  # Разрешает все источники (не рекомендуется для production)

# ???????????
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ??? ?????????? ????? ?? ?????????
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
