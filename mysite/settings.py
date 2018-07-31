"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9ni6@d@fi$^9z9gf^3dg9s7=6i*@y##%*9*c24wpuxfx((2o#^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = True

# LOCALHOST = '127.0.0.1:8000'

# ALLOWED_HOSTS = ["manbu.pythonanywhere.com"]
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user',
    'blog',
    'comment',
    'ckeditor',
    'ckeditor_uploader',
    'captcha',
    'like',
    'doudou',
    'word',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysite',
        'USER': 'root',
        'HOST':'127.0.0.1',
        'PASSWORD':'19900123',
        'PORT':'3306',
        'OPTIONS': {
            'init_command': "SET sql_mode = traditional",
            'charset': 'utf8mb4',
            }
        },
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfies")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# meida
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 配置ckeditor路径
CKEDITOR_UPLOAD_PATH = 'upload/'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar_MyConfig': [

            {'name': 'clipboard', 'items': ['Undo', 'Redo', '-', 'Cut', 'Copy']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv']},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'Smiley','Iframe','SpecialChar']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-']},
            {'name': 'tools', 'items': ['CodeSnippet', 'Maximize']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'FontSize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'CopyFormatting', 'RemoveFormat']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'paragraph',
             'items': ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'document', 'items': ['Source']},
        ],
        'toolbar': 'MyConfig',
        'extraPlugins': 'codesnippet',
        'width':'auto',
        'height':'180',
        'tabSpaces': 4,
        'removePlugins':'elementspath',
        'resize_enabled':False,
    },
    'comment':{
        'toolbar_MyConfig': [
            {'name': 'insert','items': ['Smiley']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        ],
        'smiley_images': [ '9.gif', '10.gif',
                          '11.gif', '12.gif', '13.gif', '14.gif', '15.gif', '16.gif', '17.gif', '18.gif', '19.gif',
                          '20.gif',
                          '21.gif', '22.gif', '23.gif', '24.gif', '25.gif', '26.gif', '27.gif', '28.gif', '29.gif',
                          '30.gif',
                          '31.gif', '32.gif', '33.gif', '34.gif', '35.gif', '36.gif', '37.gif', '38.gif', '39.gif',
                          '40.gif',
                          '41.gif', '42.gif', '43.gif', '44.gif', '45.gif', '46.gif', '47.gif', '48.gif', '49.gif',
                          '50.gif',
                          '51.gif', '52.gif', '53.gif', '54.gif', '55.gif',
                          ],  # 使用哪些表情
        'smiley_columns': 10,  # 控制行表情个数，此处为10个
        'smiley_descriptions': [],
        'toolbar': 'MyConfig',
        'width':'200%',
        'height':'120%',
        'tabSpaces': 4,
        'removePlugins':'elementspath',
        'resize_enabled':False,
        'toolbarLocation': 'bottom',
        'language' : 'zh-hans',
        'uiColor' :'#97CBFF',
        'fontSize_defaultLabel':'12px',
        'toolbarStartupExpanded':False,
        'toolbarCanCollapse': True,

    },
    'message':{
        'toolbar_MyConfig': [
            {'name': 'insert','items': ['Smiley','Image']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
        ],
        'smiley_images': [ '9.gif', '10.gif',
                          '11.gif', '12.gif', '13.gif', '14.gif', '15.gif', '16.gif', '17.gif', '18.gif', '19.gif',
                          '20.gif',
                          '21.gif', '22.gif', '23.gif', '24.gif', '25.gif', '26.gif', '27.gif', '28.gif', '29.gif',
                          '30.gif',
                          '31.gif', '32.gif', '33.gif', '34.gif', '35.gif', '36.gif', '37.gif', '38.gif', '39.gif',
                          '40.gif',
                          '41.gif', '42.gif', '43.gif', '44.gif', '45.gif', '46.gif', '47.gif', '48.gif', '49.gif',
                          '50.gif',
                          '51.gif', '52.gif', '53.gif', '54.gif', '55.gif',
                          ],  # 使用哪些表情
        'smiley_columns': 10,  # 控制行表情个数，此处为10个
        'smiley_descriptions': [],
        'toolbar': 'MyConfig',
        'width':'185%',
        'height':'120%',
        'tabSpaces': 4,
        'removePlugins':'elementspath',
        'resize_enabled':False,
        'toolbarLocation': 'bottom',
        'language' : 'zh-hans',
        'uiColor' :'#FFC78E',
        'fontSize_defaultLabel':'12px',
        'toolbarStartupExpanded':True,
    }
}


# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'xapian_backend.XapianEngine',
#         'PATH': os.path.join(os.path.dirname(__file__), 'xapian_index'),
#     },
# }


# 配置邮箱

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '562729270@qq.com'
EMAIL_HOST_PASSWORD = 'uwajzkojbgxwbefj'
EMAIL_SUBJECT_PREFIX = '[漫步的博客]'
EMAIL_USE_TLS = True