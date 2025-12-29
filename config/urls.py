from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

from landing.views import RegisterView, LoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "accounts/registration/",
        RegisterView.as_view(),
        name="registration"
    ),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("work-space/", include("task.urls", namespace="task")),
    path("", include("landing.urls", namespace="landing"))
] + debug_toolbar_urls()
