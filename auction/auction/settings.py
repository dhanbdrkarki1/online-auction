from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['bidme.com','localhost','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django.contrib.humanize',
    'django.contrib.postgres',
    'social_django',
    'easy_thumbnails',
    'rest_framework',
    'auctionapp.apps.AuctionappConfig',
    'account.apps.AccountConfig',
    'lot.apps.LotConfig',
    'chat.apps.ChatConfig',
    'api.apps.ApiConfig',
    'payment.apps.PaymentConfig',
    'reviews.apps.ReviewsConfig',


]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]


# SOCIAL AUTH SETTINGS START
# recommended to use the built-in JSONB field to store the extracted extra_data When using PostgreSQL
# SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_URL_NAMESPACE = "social"
AUTHENTICATION_BACKENDS = [
     'django.contrib.auth.backends.ModelBackend',
     'social_core.backends.google.GoogleOAuth2',
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_PIPELINE = [
 'social_core.pipeline.social_auth.social_details',
 'social_core.pipeline.social_auth.social_uid',
 'social_core.pipeline.social_auth.auth_allowed',
 'social_core.pipeline.social_auth.social_user',
 'social_core.pipeline.user.get_username',
 'social_core.pipeline.user.create_user',

 # adding function to auth pipeline
 'account.authentication.create_profile',
 'social_core.pipeline.social_auth.associate_user',
 'social_core.pipeline.social_auth.load_extra_data',
 'social_core.pipeline.user.user_details',
]

SOCIAL_AUTH_USER_FIELDS = ['first_name', 'last_name', 'email' ]
# END


ROOT_URLCONF = 'auction.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  
                'social_django.context_processors.login_redirect',

                # displaying categories to all templates
                'auctionapp.context_processors.category',

            ],
        },
    },
]

WSGI_APPLICATION = 'auction.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True

AUTH_USER_MODEL = 'account.CustomUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email server configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD =  config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587

# easy thumbnail to crop images to a specific aspect ratio
THUMBNAIL_ALIASES = {
    '': {
        'home_lot_image_thumbnail': {'size': (300, 250), 'crop': 'smart', 'quality':100},
        'lot_detail_thumbnail': {'size': (700, 466), 'crop': 'smart', 'quality': 100},
        'seller_profile_image_thumbnail': {'size': (200, 200), 'crop': 'smart', 'quality': 100},

    },
}

ASGI_APPLICATION = 'auction.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
        'hosts': [('127.0.0.1', 6379)],
        },
    },
}