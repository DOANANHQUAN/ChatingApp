from .base import *

DEBUG = True

SECRET_KEY = "django-insecure-dev-secret-key-replace-this-in-production"

ALLOWED_HOSTS = ["*"]

# SQLite Database for Development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Django Channels - Local Dev Channel Layer
# During development, we can use InMemoryChannelLayer if Redis is not running.
# Uncomment the Redis configuration below when your Redis server is running.
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# Redis Channel Layer Configuration (uncomment to use)
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }

# Internal IPs for debug toolbar if needed
INTERNAL_IPS = ["127.0.0.1"]
