from config.settings.base import *


SECRET_KEY = "django-insecure-bxsv(z7zncgl!hq#mxp7w84w%eq^ta@t)y1gs*om^ai^$n1sc)"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
