# from .settings import *
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Azure App Service automatically creates an environmental variable named WEBSITE_HOSTNAME. 
# This variable contains the URL for your website. You can use this variable to determine 
# whether your application is running on Azure.
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []

# Database connection string for PostgreSQL
hostname = os.environ['DBHOST']
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql',
        'NAME'    : os.environ['DBNAME'],
        'HOST'    : hostname + ".postgres.database.azure.com",
        'USER'    : os.environ['DBUSER'],
        'PASSWORD': os.environ['DBPASS'],
        'OPTIONS': {'sslmode': 'require'}
    }
}

os.environ['debug_DBENGINE'] = DATABASES['default']['ENGINE']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Enables whitenoise for serving static files
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

