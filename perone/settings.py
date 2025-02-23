import os
from pathlib import Path
from django.contrib.messages import constants as messages

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "SECRET_KEY", "django-insecure-62di2nnbar+ejeo)m^_$_l_6-3)%jh#fy6jc@y4_kin$i_q@xv")

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["perone.onrender.com", "localhost",
                 "127.0.0.1"]  # ❌ SIN "https://" NI "/"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drinks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'perone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'perone.wsgi.application'

# 📌 USANDO SQLite CON PERSISTENCIA EN RENDER
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Mueve la base de datos a /data/
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

# Asegura que la carpeta exista
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: "danger",
    messages.SUCCESS: "success",
}
