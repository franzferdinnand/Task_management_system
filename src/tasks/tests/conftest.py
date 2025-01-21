import os
import django

def pytest_configure():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

import django_filters
print(f"django_filters is located at: {django_filters.__file__}")