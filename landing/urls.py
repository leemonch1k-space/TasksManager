from django.urls import path

from landing.views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="main-page"),
]

app_name = "landing"