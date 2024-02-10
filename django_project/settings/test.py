from django_project.settings.base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "TEST": {
            "NAME": BASE_DIR.parent / "test.sqlite3",
        },
    },
}
