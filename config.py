import os

# Config file, put all your keys and passwords and whatnot in here
WTF_CSRF_ENABLED = True
SECRET_KEY = "secret-secret"
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
