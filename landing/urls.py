from django.urls import path

from landing.views import (
    HomePageView,
    AboutPageView,
    FeaturesPageView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="main-page"),
    path("about_us/", AboutPageView.as_view(), name="about_us"),
    path("features/", FeaturesPageView.as_view(), name="features"),
]

app_name = "landing"
