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
        with transaction.atomic():
            form.instance.is_active = False
            user = form.save()
            schema = self.request.scheme
            domain = get_current_site(self.request).domain
            token = user_token_activation.make_token(user)
            try:
                EmailService.send_activation_email(
                    user=user,
                    schema=schema,
                    domain=domain,
                    token=token
                )
                messages.success(
                    self.request,
                    "Approve your email before log in."
                )
            except Exception:
                messages.error(
                    self.request,
                    "Failed to send email. Please check your address or try later."  # noqa: E501
                )
                return self.form_invalid(form)

        return super().form_valid(form)


class ActivateView(View):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None:
            if user.is_active:
                messages.info(request, "Your account is already activated.")

                return redirect("login")

            if user_token_activation.check_token(user, token):
                user.is_active = True
                user.save()

                messages.success(
                    request,
                    "Thank you for confirming your email. Now you can login to your account.",  # noqa: E501
                )
                return redirect("login")
        messages.error(
            self.request,
            "Email verification failed. Sign-up again."
        )
        return redirect("login")


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
