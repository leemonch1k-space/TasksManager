from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("work-space/", include("task.urls", namespace="task")),
    path("", include("landing.urls", namespace="landing"))
] + debug_toolbar_urls()
