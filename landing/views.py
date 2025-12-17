from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views import generic

from landing.forms import RegistrationForm

class RegisterView(generic.CreateView):
    success_url = reverse_lazy("task:home")
    form_class = RegistrationForm
    template_name = "registration/registration.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


class HomePageView(generic.TemplateView):
    template_name = "landing/index.html"
