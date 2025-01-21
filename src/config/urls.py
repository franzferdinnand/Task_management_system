from django.contrib import admin
from django.urls import path, include, re_path

from config.settings import ROOT_API


urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        f"{ROOT_API}/users/",
        include(
            ("users.urls", "users"),
            namespace="users"
        ),
    ),
    path(
        f"{ROOT_API}/tasks/",
        include(
            ("tasks.urls", "tasks"),
            namespace="tasks"
        ),
    ),
    path(
        f"{ROOT_API}/auth/",
        include(
            ("authentication.urls", "authentication"),
            namespace="authentication"
        ),
    ),
]
