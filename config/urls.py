from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include

from landing.views import RegisterView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/registration", RegisterView.as_view(), name="registration"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("work-space/", include("task.urls", namespace="task")),
    path("", include("landing.urls", namespace="landing"))
] + debug_toolbar_urls()
