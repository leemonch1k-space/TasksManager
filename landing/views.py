from django.contrib import messages
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import generic, View

from landing.forms import RegistrationForm
from landing.mixins import AnonymousRequiredMixin
from landing.services.email_service import EmailService
from landing.services.token_service import user_token_activation
from task.models import Task

User = get_user_model()


class RegisterView(
    AnonymousRequiredMixin,
    generic.FormView
):
    form_class = RegistrationForm
    template_name = "registration/registration.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        messages.success(
            self.request,
            "Account was created! Now you can login to your account."
        )
        return super().form_valid(form)


class LoginView(AnonymousRequiredMixin, auth_views.LoginView):
    template_name = "registration/login.html"


class HomePageView(AnonymousRequiredMixin, generic.TemplateView):
    template_name = "landing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.all().count()
        context["completed_tasks"] = (Task.objects
                                      .filter(is_completed=True)
                                      .count()
                                      )
        context["total_users"] = get_user_model().objects.all().count()
        return context


class AboutPageView(AnonymousRequiredMixin, generic.TemplateView):
    template_name = "landing/about.html"


class FeaturesPageView(AnonymousRequiredMixin, generic.TemplateView):
    template_name = "landing/features.html"
