"""
Django settings for FireMonitoring project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
DEBUG = True
SECRET_KEY = 'r*=%h-z)t(9dn7lqz^vx-hq9sh!n&zcu-n+u_e##!%+e(tuqw0'
ALLOWED_HOSTS = ["*"]


DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'fire_database',
        "USER": 'fire_user',
        "PASSWORD": '123456',
        "HOST": 'localhost',
        "PORT": '54320',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

CASCADE_URL = 'http://kaskad.ukmmchs.ru'




